from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.forms import forms,ModelForm
from datetime import datetime,timedelta




class Tournament(models.Model):
    tournament_name = models.CharField(max_length=100)
    date =models.DateTimeField(default=datetime.now())
    is_cricket = models.BooleanField(default=False)
    is_football = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s' %(self.tournament_name,format(self.date))


class Cricket(models.Model):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE,default='')
    cricket_match_name = models.CharField(max_length=150,default="")
    on_date = models.DateTimeField()
    updated_on = models.DateTimeField(default=datetime.now())
    preview = models.CharField(max_length=500,default="")
    para1 = models.CharField(max_length=800,default="")
    para2 = models.CharField(max_length=800,default="")
    para3 = models.CharField(max_length=800,null=True,default="")
    team1_des = models.CharField(max_length=100,null=True,default="")
    team1 = models.CharField(max_length=600,default="")
    team2_des = models.CharField(max_length=100,default="")
    team2 = models.CharField(max_length=600,default="")
    team3_des = models.CharField(max_length=100,default="")
    team3 = models.CharField(max_length=600, null=True)
    team4 = models.ImageField(default=None,null=True)
    team5 = models.ImageField(default=None,null=True)
    conclusion = models.CharField(max_length=450,default="")
    final_verdict = models.CharField(max_length=400,default="")
    image = models.ImageField(default="")

    def __str__(self):
        return '%s %s' %(self.cricket_match_name,format(self.on_date))




class Football(models.Model):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE,default='')
    football_match_name = models.CharField(max_length=150, default="")
    on_date = models.DateTimeField(default=datetime.now())
    updated_on = models.DateTimeField(default=datetime.now())
    preview = models.CharField(max_length=500, default="")
    para1 = models.CharField(max_length=800, default="")
    para2 = models.CharField(max_length=800, default="")
    para3 = models.CharField(max_length=800, null=True, default="")
    team1_des = models.CharField(max_length=100, null=True, default="")
    team1 = models.CharField(max_length=700, default="")
    team2_des = models.CharField(max_length=100, default="")
    team2 = models.CharField(max_length=700, default="")
    team3_des = models.CharField(max_length=100,default="")
    team3 = models.CharField(max_length=700, null=True)
    team4 = models.ImageField(default=None,null=True)
    team5 = models.ImageField(default=None,null=True)
    conclusion = models.CharField(max_length=450, default="")
    final_verdict = models.CharField(max_length=500, default="")
    image = models.ImageField(default="")

    def __str__(self):
        return '%s %s' %(self.football_match_name,format(self.on_date))



class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    state = models.CharField(max_length=20)
    place = models.CharField(max_length=40)
    is_active = models.BooleanField(default=False)
    credits = models.IntegerField(default=0)
    activation_code = models.IntegerField(default=828167)

    def __str__(self):
        return '%s %s'%(self.user,self.email)
class Match(models.Model):
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE)
    match_name = models.CharField(max_length=50)

    def __str__(self):
        return self.match_name

class FAQ(models.Model):
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return '%s %s'%(self.match,self.user)


class ContactUs(models.Model):
    Name = models.CharField(max_length=30)
    place = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    message = models.CharField(max_length=500)
    email = models.EmailField()
    status = models.BooleanField(default=True)
    reply = models.CharField(max_length=500,default='')

    def __str__(self):
        return '%s %s' %(self.Name,self.mobile)