from django.conf import settings
from django.shortcuts import render,get_object_or_404,redirect
from .models import UserLike
from django.contrib.auth import get_user_model


User= get_user_model()

def like_user(request, email):
    pending_like = get_object_or_404(User, email=email)
    userr=get_object_or_404(user=request.user,email=request.user)
    user_like, created= UserLike.objects.get_or_create(user=userr)
    if pending_like in user_like.liked_users.all():
        user_like.liked_users.remove(pending_like)
    else:
        user_like.liked_users.add(pending_like)

    return redirect("profile", email= pending_like.email)
