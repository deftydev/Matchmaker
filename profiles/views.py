from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404,redirect
from accounts.models import User


from likes.models import UserLike
from matcho.models import Match
from .forms import UserJobForm,ProfileForm
from .models import Profile, UserJob

@login_required
def profile_user(request):
    user=get_object_or_404(User,email=request.user)
    profile, created=Profile.objects.get_or_create(user=user)
    jobs=user.userjob_set.all()
    context={"profile":profile,
             "jobs": jobs,
             }
    return render(request,"profiles/profile_user.html",context)


@login_required
def profile_edit(request):
    title="Update profile"
    profile, created=Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None,request.FILES or None, instance=profile)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.save()
        return redirect("profile_user")
    context={
        "form" : form,
        "title": title,
    }
    return render(request,"profiles/forms.html", context)


@login_required
def profile_view(request,email):
    user=get_object_or_404(User,email=email)
    profile, created=Profile.objects.get_or_create(user=user)
    user_like, user_like_created= UserLike.objects.get_or_create(user=request.user)
    do_i_like= False
    if user in user_like.liked_users.all():
        do_i_like=True
    mutual_like= user_like.get_mutual_like(user)
    match, match_created=Match.objects.get_or_create_match(user_a=request.user,user_b=user)
    jobs=user.userjob_set.all()

    context={"profile":profile,
             "match": match,
             "jobs": jobs,
             "mutual_like":mutual_like,
             "do_i_like":do_i_like
             }
    return render(request,"profiles/profile_view.html",context)

@login_required
def job_add(request):
    title="Add Job"
    job=UserJob.objects.all()[0]
    form = UserJobForm(request.POST or None, instance=job)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.save()
        return redirect("profile_user")
    context={
        "form" : form,
        "title": title,
    }
    return render(request,"profiles/forms.html", context)


@login_required
def jobs_edit(request):
    title="Edit Jobs"
    UserJobFormset= modelformset_factory(UserJob, form=UserJobForm)
    queryset= UserJob.objects.filter(user=request.user)
    formset=UserJobFormset(request.POST or None, queryset=queryset)
    if formset.is_valid():
        instances=formset.save(commit=False)
        for instance in instances:
            instance.user=request.user
            instance.save()
        return redirect("profile_user")

    context={
        "formset" : formset,
        "title": title,
    }
    return render(request,"profiles/formset.html", context)
