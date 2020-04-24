from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index),
    path('u/<username>', views.profile),
    path('logout/', views.logout_view),
    path('register/', views.register_view),
    path('profile/', views.getProfile),
    path('profileedit/', views.profileedit),
    path('post/', views.post),
    path('posts/', views.getPosts),
    path('search/', views.searchPosts),
    path('searchvue/', views.searchPostsJSON),
    path('messages/', views.index),

    path('chat/', views.chatIndex),
    path('chat/<str:room_name>/', views.chatRoom),
]+ static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
