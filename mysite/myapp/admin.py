from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.ProfileModel)
admin.site.register(models.PostModel)
admin.site.register(models.LikeModel)
admin.site.register(models.CommentModel)