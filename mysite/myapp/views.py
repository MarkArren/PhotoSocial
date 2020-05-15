from django.http import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory
from django.db.models import Q
from django.middleware import csrf

from datetime import datetime, timezone
from math import ceil

from . import models
from . import forms



def chatRoom(request, room_name):
    if request.user.is_authenticated:
        return render(request, 'myapp/chatroom.html', {
            'room_name': room_name,
            'username': request.user.username
        })
    else:
        return redirect("/")

def messages(request):
    if request.user.is_authenticated:
        followingList = getCurrentProfile(request).toDictFollowers()
        print(followingList)
        for person in followingList:
            print(person.user.username)
        context = {
            "following": followingList,
            "room_name": request.user.username,
            'username': request.user.username
        }
        return render(request, 'myapp/chats.html', context)
    else:
        return redirect("/")


def index(request):
    # Display home page
    if request.user.is_authenticated:
        if request.method == "POST":
            if 'type' in request.POST:
                # Process post requests for like, comment, delete and follow
                if request.POST["type"] == "like":
                    return likePost(request)
                elif request.POST["type"] == "comment":
                    return commentPost(request)
                elif request.POST["type"] == "delete":
                    return deletePost(request)
                elif request.POST["type"] == "follow":
                    return followProfile(request)

        return render(request, 'myapp/index.html')

    # Display log in page
    else:
        # Attempt to log in user
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, 'Username or password incorrect')
                return redirect("/")
        # Else show log in form
        else:
            return render(request, 'myapp/login.html')

def getPosts(request):
    profile = getCurrentProfile(request)
    postObjects = models.PostModel.objects.filter(Q(profile__in=(profile.following.all())) | Q(profile=profile)).order_by('-date')
    postsList = []

    print(type(postObjects))

    # Loop through data backwards parsing values into the new list
    for i in range(len(postObjects)):
        post = postObjects[i]
        tempPost = post.toDictExtra(request, profile)
        postsList.append(tempPost.copy())

    context = {
        "posts": postsList,
    }

    return JsonResponse(context)

def searchPosts(request):
    if request.method == "GET":
        return render(request, "myapp/search.html")

def searchPostsJSON(request):    
    if request.method == "GET":
        if 'search' in request.GET:    
            postsList = []
            search = request.GET["search"]

            profile = getCurrentProfile(request)
            postObjects = models.PostModel.objects.filter(
                Q(profile__user__username__icontains=search) | 
                Q(caption__icontains=search) | 
                Q(location__icontains=search)
                ).order_by('-date')


            # Loop through data parsing values into the new list
            for i in range(len(postObjects)):
                post = postObjects[i]
                postsList.append(post.toDictExtra(request, profile).copy())

            context = {
                "posts": postsList,
            }
            print(len(postsList))      

            return JsonResponse(context)
            # return render(request, "myapp/search.html", context=context)

    return redirect("/")



def likePost(request):
    if request.method == "POST":
        post = models.PostModel.objects.get(id=request.POST["post"])

        # Check if user has already liked post
        try:
            # Removes like from the post
            likes = models.LikeModel.objects.get(
                post=post, profile=getCurrentProfile(request))
            likes.delete()
        except models.LikeModel.DoesNotExist:
            # Adds a like to a post
            like = models.LikeModel(
                post=post, profile=getCurrentProfile(request))
            like.save(post=post, profile=getCurrentProfile(request))

    return redirect("/")

def commentPost(request):
    if request.method == "POST":
        post = models.PostModel.objects.get(id=request.POST["post"])
        comment = request.POST["comment"]
        parentComment = request.POST["parentComment"]
        
        # Get parent comment if specified
        if parentComment == "":
            parentComment = None
        else:
            parentComment = models.CommentModel.objects.get(id=request.POST["parentComment"])

        comment = models.CommentModel(post=post, profile=getCurrentProfile(request), comment=comment, parentComment=parentComment)
        comment.save(post=post, profile=getCurrentProfile(request))

    return redirect("/")

def deletePost(request):
    if request.method == "POST":
        post = models.PostModel.objects.get(id=request.POST["post"])

        # Check if its user post
        profile = getCurrentProfile(request)
        if post.profile == profile:
            print("owns post... deleting")
            post.delete()

    return redirect("/")


# Get profile page
def profile(request,username):
    # if request.method == "GET":
    #     if 'type' in request.POST:
    #         if request.GET["type"] == "profile":
    #             return getProfile(request, username)
    return render(request, 'myapp/profile.html')

# Get profile info
def getProfile(request):
    # Diplays users profile if it exists
    try:
        # Get username from get request
        if 'username' in request.GET:
            username = request.GET["username"]
        else:
            raise Http404
        # Get users profile
        userObject = User.objects.get(username=username)
        profileObject = models.ProfileModel.objects.filter(user=userObject)[0]

        # Get users posts in reverse order
        postObjects = models.PostModel.objects.filter(profile=profileObject).order_by('-date')
        postsList = []
        
        # Get all post objects
        for i in range(len(postObjects)):
            post = postObjects[i]
            tempPost = {}
            tempPost["id"] = post.id
            tempPost["image"] = post.image.url
            postsList += [tempPost]
    
        # Get all profile info
        profile = dict(profileObject.toDict())

        # Checks if the logged in user is following the user
        if request.user.is_authenticated:
            if len(getCurrentProfile(request).following.filter(id=profileObject.id)):
                profile["isFollowing"] = True
            else:
                profile["isFollowing"] = False

        # Check if user is current user
        if profileObject == getCurrentProfile(request):
            profile["isCurrentUser"] = True
        else:
            profile["isCurrentUser"] = False

        profile["postRows"] = int(ceil(len(postObjects) / 3))

        context = {
            'profile' : profile,
            'posts' : postsList,
        }
        return JsonResponse(context)
    except ObjectDoesNotExist:
        raise Http404


def profileedit(request):
    if request.user.is_authenticated:
        # Get current user and profile
        profile = getCurrentProfile(request)
        user = profile.user

        if request.method == "POST":
            userForm = forms.UserUpdateForm(request.POST, instance=user)
            profileForm = forms.ProfileForm(request.POST, request.FILES, instance=profile)

            if userForm.is_valid() and profileForm.is_valid():
                # Save in to database
                user.save()
                profile.save()
                print("saved profile")
                return redirect("/u/" + user.username)
            else:
                print(userForm.errors)
                print("not valid")
                print("user " + str(userForm.is_valid()))
                print("profile " + str(profileForm.is_valid()))
        else:
            # Return page with forms
            userForm = forms.UserUpdateForm(instance=user)
            profileForm = forms.ProfileForm(instance=profile)
        context = {
            "form": userForm,
            'profileForm': profileForm
        }
        return render(request, "myapp/profileedit.html", context=context)
    else:
        return redirect("/")

def followProfile(request):
    if request.method == "POST":
        profile = getCurrentProfile(request)
        otherProfile = models.ProfileModel.objects.get(id=request.POST["profile"])

        # Check if user is already following profile
        if len(profile.following.filter(id=otherProfile.id)):
            # Unfollow profile
            follow = profile.following.filter(id=otherProfile.id)
            print(follow)
            profile.following.remove(otherProfile)
            profile.save()
            print("unfollowed " + otherProfile.user.username)
        else:
             # Follow profile
            profile.following.add(otherProfile)
            profile.save()
            print("followed " + otherProfile.user.username)

    return redirect("/")


# Post page
def post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            return makePost(request)
        else:
            # Return page with form
            form = forms.PostForm()
            context = {
                "form": form
            }
            return render(request, 'myapp/post.html', context)
    else:
        return redirect("/")


def getNotifications(request):
    profile = getCurrentProfile(request)
    notificationObjects = models.NotificationModel.objects.filter(notifier=profile.id).order_by('-date')
    notificationList = []

    # Loop through data backwards parsing values into the new list
    for i in range(len(notificationObjects)):
        notification = notificationObjects[i]
        tempNotification = notification.toDict()
        notificationList.append(tempNotification.copy())

    context = {
        "notifications": notificationList,
    }

    return JsonResponse(context)


# Makes post in database
def makePost(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            # profile =  models.ProfileModel.objects.filter(user=request.user.id)

            # form.profile = profile
            form.save(request)
            return redirect("/")
        else:
            context = {
                "form": form
            }
            return render(request, 'myapp/post.html', context)
    return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("/")


def register_view(request):
    # profileFormSet = modelformset_factory(models.ProfileModel, fields="")

    if request.method == "POST":
        userForm = forms.RegistrationForm(request.POST)
        profileForm = forms.ProfileForm(request.POST, request.FILES)

        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save()

            # Create profile for user
            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()

            # Login user
            user = authenticate(
                request, username=userForm.cleaned_data['username'], password=userForm.cleaned_data['password1'])
            login(request, user)

            return redirect("/")
    else:
        userForm = forms.RegistrationForm()
        profileForm = forms.ProfileForm()
    context = {
        "form": userForm,
        'profileForm': profileForm
    }
    return render(request, "myapp/register.html", context=context)


def getCurrentProfile(request):
    return models.ProfileModel.objects.filter(user=request.user.id)[0]