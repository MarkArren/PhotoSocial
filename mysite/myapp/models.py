from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timezone
from django.middleware import csrf

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

    def toDict(self):
        postObjects = PostModel.objects.filter(profile=self).order_by('-date')

        profile={}
        profile["id"] = self.id
        profile["username"] = self.user.username
        profile["name"] = str(self)
        if (self.profilePicture):
            profile["image"] = self.profilePicture.url
        else:
            profile["image"] = "/media/placeholder/300x300.png"
        profile["bio"] = self.bio

        profile["posts"] = str(len(postObjects))
        profile["followers"] = str(self.followedBy.all().count())
        profile["following"] = str(self.following.all().count())

        return profile




class PostModel(models.Model):
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)

    image = models.ImageField(
        max_length=144,
        upload_to='uploads/%Y/%m/%d/')
    
    caption = models.CharField(max_length=512, blank=True)
    location = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)


    def toDict(self):
        likeObjects = LikeModel.objects.filter(post=self)
        commentObjects = CommentModel.objects.filter(post=self)

        tempPost = {}
        tempPost["id"] = self.id
        tempPost["image"] = self.image.url
        tempPost["caption"] = self.caption
        tempPost["location"] = self.location
        tempPost["username"] = self.profile.user.username
        tempPost["likeCount"] = str(len(likeObjects))
        tempPost["commentCount"] = str(len(commentObjects))
        if isinstance(self.date, datetime):
            tempPost["date"] = getTimeDifference(self.date)


        # In list of comments store a dict with a comment and its children
        parentCommentObjects = CommentModel.objects.filter(post=self, parentComment__isnull=True)
        comments = []
        for comment in parentCommentObjects:
            commentDict = {}
            commentDict["comment"] = comment.toDict()

            # Create list of child comments
            childCommentsList = []
            childComments = CommentModel.objects.filter(post=self, parentComment=comment)
            for childComment in childComments:
                childCommentsList.append(childComment.toDict())
            
            commentDict["childComments"] = childCommentsList
            comments.append(commentDict)
            # comments.append(comment.toDict())
        tempPost["comments"] = comments

        return tempPost

    def toDictExtra(self, request, profile):
        tempPost = self.toDict()
        tempPost["isOwnPost"] = False
        tempPost["liked"] = False

       
        if request.user.is_authenticated:
             # Checks if the logged in user has liked the post or not
            try:
                LikeModel.objects.get(
                    post=self, profile=profile)
                tempPost["liked"] = True
            except LikeModel.DoesNotExist:
                pass

            # Checks if it is users own post
            if self.profile == profile:
                tempPost["isOwnPost"] = True
        
        tempPost["token"] = csrf.get_token(request)
        return tempPost




class LikeModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)
    date = models.DateTimeField(auto_now_add=True)
    parentComment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='childComment')

    def __str__(self):
        return self.comment

    def toDict(self):
        tempComment = {}
        tempComment["id"] = self.id
        tempComment["username"] = self.profile.user.username
        tempComment["comment"] = self.comment
        tempComment["profilePicture"] = self.profile.profilePicture.url

        if self.parentComment:
            tempComment["parentComment"] = self.parentComment.id

        return tempComment

def getTimeDifference(time):
    difference = datetime.now(timezone.utc) - time
    hours = difference.seconds / 3600

    if difference.days >= 365:
        return time.strftime("%d %B %Y")
    elif difference.days >= 7:
        return time.strftime("%d %B")
    elif difference.days >= 1:
        return str(int(difference.days)) + " days ago"
    elif hours > 1:
        return str(int(hours)) + " hours ago"
    elif difference.seconds >= 60:
        return str(int(difference.seconds / 60)) + " minutes ago"
    else:
        return str(int(difference.seconds)) + " seconds ago"