# Generated by Django 3.0.3 on 2020-05-31 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('likes', '0008_auto_20200601_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlike',
            name='id',
            field=models.AutoField(auto_created=True, default='', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userlike',
            name='userr',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='liker', to=settings.AUTH_USER_MODEL, to_field='email'),
        ),
    ]
