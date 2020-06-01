from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from jobs.models import  Job,Employer,Location
from likes.models import UserLike
from matcho.models import Match,PositionMatch,EmployerMatch,LocationMatch

from questions.forms import UserResponseForm
from questions.models import Question
from accounts.forms import SignupForm
from accounts.models import User




def home(request):
    if request.user.is_authenticated:
        matches=Match.objects.get_matches_with_percent(request.user)[:6]
        positions=PositionMatch.objects.filter(user=request.user)[:6]
        if positions.count() > 0:
            positions[0].check_update(20)
        locations=LocationMatch.objects.filter(user=request.user)[:6]
        employers=EmployerMatch.objects.filter(user=request.user)[:5]
        mutual_likes= UserLike.objects.get_all_mutual_likes(request.user,4)
        new_user=False
        if len(mutual_likes) == 0 and len(matches)== 0:
            new_user=True
		# for match in matches:
		# 	job_set=match[0].userjob_set.all()
		# 	if job_set.count() > 0:
		# 		for job in job_set:
		# 			if job.position not in positions:
		# 				positions.append(job.position)
		# 				the_job=Job.objects.get(text__iexact=job.position)
		# 				jobmatch, created=PositionMatch.objects.get_or_create(user=request.user,job=the_job)
		# 				try:
		# 					the_job=Job.objects.get(text__iexact=job.position)
		# 					jobmatch, created=JobMatch.objects.get_or_create(user=request.user,job=the_job)
		# 				except:
		# 					pass
		# 			if job.location not in locations:
		# 				locations.append(job.location)
		# 				try:
		# 					the_loc=Location.objects.get(name__iexact=job.location)
		# 					locmatch, created=LocationMatch.objects.get_or_create(user=request.user,location=the_loc)
		# 					print(locmatch)
		# 				except:
		# 					pass
		# 			if job.employer_name not in employers:
		# 				employers.append(job.employer_name)
		# 				try:
		# 					the_employer=Employer.objects.get(name__iexact=job.employer_name)
		# 					empymatch, created=EmployerMatch.objects.get_or_create(user=request.user,employer=the_employer)
		# 					print(empymatch)
		# 				except:
		# 					pass
        question_instance=None
        queryset = Question.objects.get_unanswered(request.user).order_by('-timestamp')
        if queryset.count()>0:
            question_instance= queryset.order_by("?").first()
        question_form=UserResponseForm()
        context = {
        "queryset": queryset,
        "matches":matches,
        "positions":positions,
        "locations":locations,
        "employers":employers,
        "mutual_likes":mutual_likes,
        "new_user":new_user,
        "question_form":question_form,
        "question_instance":question_instance
        }
        return render(request, "dashboard/home.html", context)
    return render(request, "accounts/signup.html", {})
