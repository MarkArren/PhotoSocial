# Generated by Django 3.0.5 on 2020-05-06 22:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20200506_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationmodel',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]