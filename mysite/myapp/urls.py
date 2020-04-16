from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index),
    path('u/<username>', views.profile),
    path('logout/', views.logout_view),
    path('register/', views.register_view),
    path('profile/', views.index),
    path('post/', views.post),
    path('messages/', views.index),
]
