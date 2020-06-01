# Generated by Django 3.0.3 on 2020-05-31 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlike',
            name='id',
        ),
        migrations.AlterField(
            model_name='userlike',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='liker', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]