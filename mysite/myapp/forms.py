from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from . import models
from .models import ProfileModel


class PostForm(forms.Form):
    image = forms.ImageField(label="Upload Image", required=True)
    caption = forms.CharField(label="Caption", max_length=512, required=False)
    location = forms.CharField(label="Location", max_length=50, required=False)

    def save(self, request):
        postInstance = models.PostModel()
        postInstance.image = self.cleaned_data["image"]
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
        fields = ('profilePicture', 'fullname', 'email' ,'bio')

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