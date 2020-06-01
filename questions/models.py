from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.db.models import Q

class QuestionManager(models.Manager):
    def get_unanswered(self,user):
        q1=Q(useranswer__user=user)
        qs= self.exclude(q1)
        return qs


class Question(models.Model):
    text=models.TextField()
    active=models.BooleanField()
    draft=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True, auto_now=False)

    objects=QuestionManager()

    def __str__(self):
        return self.text[:15]

class Answer(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    text=models.TextField()
    active=models.BooleanField()
    draft=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.text[:15]

LEVELS=(
    ('Mandatory','Mandatory'),
    ('Very Important','Very Important'),
    ('Somewhat Important','Somewhat Important'),
    ('Not Important','Not Important')
)


class UserAnswer(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    my_answer= models.ForeignKey(Answer, related_name='user_answer',on_delete=models.CASCADE)
    my_answer_importance=models.CharField(max_length=50, choices=LEVELS)
    my_points=models.IntegerField(default=-1)
    their_answer=models.ForeignKey(Answer, null=True, blank=True, related_name='match_answer',on_delete=models.CASCADE)
    their_importance=models.CharField(max_length=50, choices=LEVELS)
    their_points=models.IntegerField(default=-1)
    timestamp= models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.my_answer.text[:10]

def score_importance(importance_level):
    if importance_level == "Mandatory":
        points=300
    elif importance_level == "Very Important":
        points=200
    elif importance_level == "Somewhat Important":
        points=50
    elif importance_level == "Not Important":
        points=0
    else:
        points=0
    return points

def update_user_answer_score(sender, instance,*args,**kwargs):
    my_points= score_importance(instance.my_answer_importance)
    instance.my_points=my_points
    their_points= score_importance(instance.their_importance)
    instance.their_points=their_points

pre_save.connect(update_user_answer_score,sender=UserAnswer)
