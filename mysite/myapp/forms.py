from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from . import models
from .models import ProfileModel

from io import BytesIO
from PIL import Image, ExifTags
from django.core.files import File


def compressImage(image):
	maxWidth = 440
	# Open image and get bytes
	imageTmp = Image.open(image).convert('RGB')
	imageIO = BytesIO()

	try:
		# Rotate image if 'Orientation' included in metadata
		# From https://stackoverflow.com/questions/13872331/rotating-an-image-with-orientation-specified-in-exif-using-python-without-pil-in
		for orientation in ExifTags.TAGS.keys():
			if ExifTags.TAGS[orientation]=='Orientation':
				break
		exif=dict(imageTmp.getexif().items())
		if exif[orientation] == 3:
			imageTmp=imageTmp.rotate(180, expand=True)
		elif exif[orientation] == 6:
			imageTmp=imageTmp.rotate(270, expand=True)
		elif exif[orientation] == 8:
			imageTmp=imageTmp.rotate(90, expand=True)
	except (AttributeError, KeyError, IndexError):
		pass

	# Get image attributes
	width, height = imageTmp.size
	newWidth = width
	newHeight = height

	# Check if if image needs to be cropped
	crop = False
	if width/height > 1.7:
		# Image is too wide so cut width
		ratio = height/9
		newWidth = 16 * ratio
		newHeight = height
		crop = True
		print("too wide")
	elif width/height < 0.8:
		# image is too tall so cut height
		ratio = width / 8
		newWidth = width
		newHeight = 10 * ratio
		crop = True
		print("too tall")
	if crop:
		# Crop
		left = (width - newWidth) / 2
		top = (height - newHeight)/2
		right = (width + newWidth)/2
		bottom = (height + newHeight)/2
		imageTmp = imageTmp.crop((left, top, right, bottom))
		print("cropped")

	# Resize image
	ratio = maxWidth/newWidth
	newWidth = newWidth * ratio
	newHeight = newHeight * ratio
	imageTmp = imageTmp.resize((int(newWidth), int(newHeight)))
	print("resized")

	

	# Convert to bytes, save and compress
	imageTmp.save(imageIO, format='JPEG', optimize=True, quality=60)
	return File(imageIO, name=image.name)


class PostForm(forms.Form):
	image = forms.ImageField(label="Upload Image", required=True)
	caption = forms.CharField(label="Caption", max_length=512, required=False, widget=forms.TextInput(attrs={'placeholder': 'Caption'}))
	location = forms.CharField(label="Location", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Location'}))

	def save(self, request):
		postInstance = models.PostModel()
		postInstance.image = compressImage(self.cleaned_data["image"])
		postInstance.caption = self.cleaned_data["caption"]
		postInstance.location = self.cleaned_data["location"]

		profile = models.ProfileModel.objects.filter(user=request.user.id)
		postInstance.profile = profile[0]

		postInstance.save()
		return postInstance

# class PostForm(ModelForm):
#     class meta:
#         model = models.PostModel
#         fields = ('image', 'caption', 'location')


def must_be_unique_email(value):
	user = User.objects.filter(email=value)
	if len(user) > 0:
		raise forms.ValidationError("Email Already Exists")
	return value


def must_be_unique_username(value):
	user = User.objects.filter(username=value)
	if len(user) > 0:
		raise forms.ValidationError("Username Already Exists")
	return value


class RegistrationForm(UserCreationForm):
	# email = forms.EmailField(
	#     label="Email",
	#     required=True,
	#     validators=[EmailValidator]
	# )

	username = forms.CharField(label='Username',
							   required=True,
							   max_length=30
							   )

	class Meta:
		model = User
		fields = ("username",
				  "password1", "password2")

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		# user.email = self.cleaned_data["email"]

		if commit:
			user.save()
		return user

	# def __init__(self, *args, **kwargs):
	#     super(RegistrationForm, self).__init__(*args, **kwargs)
	#     self.fields['fullname'] = user.first_name + user.last_name


class ProfileForm(ModelForm):
	class Meta:
		model = ProfileModel
		fields = ('profilePicture', 'fullname', 'email', 'bio')

class UserUpdateForm(forms.ModelForm):       
    class Meta:
        model = User
        fields = ('username', 'email') 


# class ProfileForm(forms.Form):
#     profilePicture = forms.ImageField(label="Profile Picture", required=False)
#     bio = forms.CharField(label="Bio", max_length=512, required=False)

#     def save(self, request):
#         profileInstance = models.PostModel()
#         postInstance.user = request.user
#         profileInstance.profilePicture = self.cleaned_data["profilePicture"]
#         profileInstance.bio = self.cleaned_data["bio"]

#         profileInstance.save()
#         return profileInstance
