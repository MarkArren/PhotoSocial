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



def index(request):
    # Display home page
    if request.user.is_authenticated:
        if request.method == "POST":
            if 'type' in request.POST:
                # POST request to like post
                if request.POST["type"] == "like":
                    return likePost(request)
                # POST request to comment on post
                elif request.POST["type"] == "comment":
                    print("TODO: comment")
                elif request.POST["type"] == "follow":
                    return followProfile(request)
                elif request.POST["type"] == "delete":
                    return deletePost(request)

            
        elif request.method == "GET":
            print("GET")
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

        likeObjects = models.LikeModel.objects.filter(post=post)
        commentObjects = models.CommentModel.objects.filter(post=post)


        tempPost = {}
        tempPost["id"] = post.id
        tempPost["image"] = post.image.url
        tempPost["caption"] = post.caption
        tempPost["location"] = post.location
        tempPost["username"] = post.profile.user.username

        if isinstance(post.date, datetime):
            tempPost["date"] = getTimeDifference(post.date)

        tempPost["likes"] = str(len(likeObjects))
        tempPost["comments"] = str(len(commentObjects))
        tempPost["isOwnPost"] = False

       
        if request.user.is_authenticated:
             # Checks if the logged in user has liked the post or not
            try:
                models.LikeModel.objects.get(
                    post=post, profile=getCurrentProfile(request))
                tempPost["liked"] = True
            except models.LikeModel.DoesNotExist:
                tempPost["liked"] = False

            # Checks if it is users own post
            if post.profile == profile:
                tempPost["isOwnPost"] = True
        
        tempPost["token"] = csrf.get_token(request)
        postsList += [tempPost]

    context = {
        "posts": postsList,
    }

    return JsonResponse(context)

def searchPosts(request):
    if request.method == GET:
        if 'search' in request.GET:
            search = request.GET["search"]

            postObjects = models.PostModel.objects.filter
            (
            Q(profile__icontains=search) | 
            Q(caption__icontains=search) | 
            Q(location__icontains=search)
            ).order_by('-date')

             # Loop through data backwards parsing values into the new list
            for i in range(len(postObjects)):
                post = postObjects[i]

                likeObjects = models.LikeModel.objects.filter(post=post)
                commentObjects = models.CommentModel.objects.filter(post=post)


                tempPost = {}
                tempPost["id"] = post.id
                tempPost["image"] = post.image.url
                tempPost["caption"] = post.caption
                tempPost["location"] = post.location
                tempPost["username"] = post.profile.user.username

                if isinstance(post.date, datetime):
                    tempPost["date"] = getTimeDifference(post.date)

                tempPost["likes"] = str(len(likeObjects))
                tempPost["comments"] = str(len(commentObjects))

                # Checks if the logged in user has liked the post or not
                if request.user.is_authenticated:
                    try:
                        models.LikeModel.objects.get(
                            post=post, profile=getCurrentProfile(request))
                        tempPost["liked"] = True
                    except models.LikeModel.DoesNotExist:
                        tempPost["liked"] = False

                postsList += [tempPost]

            context = {
                "posts": postsList,
                "token": django.middleware.csrf.get_token(request)
            }

            return JsonResponse(context)
            

        pass



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
            like.save()

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
        profile={}
        profile["id"] = profileObject.id
        profile["username"] = userObject.username
        profile["name"] = str(profileObject)
        if (profileObject.profilePicture):
            profile["image"] = profileObject.profilePicture.url
        else:
            profile["image"] = "/media/placeholder/300x300.png"
        profile["bio"] = profileObject.bio

        profile["posts"] = str(len(postObjects))
        profile["followers"] = str(profileObject.followedBy.all().count())
        profile["following"] = str(profileObject.following.all().count())

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
            userForm = forms.RegistrationForm(request.POST, instance=user)
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
            userForm = forms.RegistrationForm(instance=user, initial={'fullname':user.first_name + ' ' + user.last_name})
            profileForm = forms.ProfileForm(instance=profile)
        context = {
            "form": userForm,
            'profileForm': profileForm
        }
        return render(request, "myapp/profileedit.html", context=context)
    else:
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