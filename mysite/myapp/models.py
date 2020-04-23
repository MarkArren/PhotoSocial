from django.db import models
from django.contrib.auth.models import User


# Saves users profile picture to /profiles/{username}/profilepicture.{ext}
def profilePicturePath(instance, filename):
    return 'profiles/' + instance.user.username + '/profilepicture.' +  filename.split('.')[-1]


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=60, blank=True)
    email = models.EmailField(unique=True)
    profilePicture = models.ImageField(
        max_length=144,
        upload_to=profilePicturePath,
        blank=True)
    bio = models.CharField(max_length=512, blank=True)
    following = models.ManyToManyField('self', related_name='followedBy', symmetrical=False)

    def __str__(self):
        return self.fullname
        # name = self.user.first_name + self.user.last_name
        # if name == "":
        #     return self.user.username
        # return name




class PostModel(models.Model):
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)

    image = models.ImageField(
        max_length=144,
        upload_to='uploads/%Y/%m/%d/')
    
    caption = models.CharField(max_length=512, blank=True)
    location = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)

class LikeModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)
    date = models.DateTimeField(auto_now_add=True)
    parentComment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='childComment')

    def __str__(self):
        return self.comment
