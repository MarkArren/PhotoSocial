from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist

from . import models
from . import forms


def index(request):
    # Display home page
    if request.user.is_authenticated:
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


def profile(request, username):
    # Diplays users profile if it exists
    try:
        User.objects.get(username=username)
        return render(request, 'myapp/profile.html', {'username': username})
    except ObjectDoesNotExist:
        raise Http404


def post(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/post.html')
    else:
        return redirect("/")



def logout_view(request):
    logout(request)
    return redirect("/")


def register_view(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            # Login user
            user = authenticate(
                request, username=form_instance.cleaned_data['username'], password=form_instance.cleaned_data['password1'])
            login(request, user)

            return redirect("/")
            # print("Hi")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form": form_instance,
    }
    return render(request, "myapp/register.html", context=context)
