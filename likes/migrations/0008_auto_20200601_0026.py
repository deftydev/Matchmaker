# Generated by Django 3.0.3 on 2020-05-31 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0007_auto_20200601_0013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlike',
            old_name='user',
            new_name='userr',
        ),
    ]
