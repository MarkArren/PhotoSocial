from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


def must_be_unique(value):
    user = User.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already Exists")
    return value


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    username = forms.CharField(label='Username',
                               required=True,
                               max_length=30,
                               validators=[must_be_unique]
                               )

    fullname = forms.CharField(
        label="Fullname",
        max_length=70
    )

    class Meta:
        model = User
        fields = ("email", "fullname", "username",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]

        names = self.cleaned_data["fullname"].split(' ', 1)

        if len(names) >= 1 and names[0] is not None:
            user.first_name = names[0]
        if len(names) >= 2 and names[1] is not None:
            user.last_name = names[1]

        if commit:
            user.save()
        return user
