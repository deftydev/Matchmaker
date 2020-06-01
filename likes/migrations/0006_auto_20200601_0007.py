# Generated by Django 3.0.3 on 2020-05-31 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('likes', '0005_auto_20200601_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlike',
            name='liked_users',
        ),
        migrations.AddField(
            model_name='userlike',
            name='liked_users',
            field=models.ManyToManyField(blank=True, related_name='liked_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='liker', serialize=False, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]