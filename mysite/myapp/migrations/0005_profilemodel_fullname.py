# Generated by Django 3.0.5 on 2020-04-21 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20200417_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='fullname',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
