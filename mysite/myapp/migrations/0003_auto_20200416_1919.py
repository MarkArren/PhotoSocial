# Generated by Django 3.0.5 on 2020-04-17 02:19

from django.db import migrations, models
import django.db.models.deletion
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20200416_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilemodel',
            name='profileImage',
        ),
        migrations.AddField(
            model_name='profilemodel',
            name='bio',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='profilemodel',
            name='profilePicture',
            field=models.ImageField(blank=True, max_length=144, upload_to=myapp.models.profilePicturePath),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='parentComment',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.CommentModel'),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='caption',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='location',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
