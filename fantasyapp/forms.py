from .models import *
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from django import forms

class userform(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password']

class userprofileform(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user','is_active','credits','activation_code']





class cricketform(ModelForm):
    preview = forms.CharField(widget=forms.Textarea)
    para1 = forms.CharField(widget=forms.Textarea)
    para2 = forms.CharField(widget=forms.Textarea)
    team1 = forms.CharField(widget=forms.Textarea,)
    team2 = forms.CharField(widget=forms.Textarea)
    team3 = forms.CharField(widget=forms.Textarea)
    conclusion = forms.CharField(widget=forms.Textarea)
    final_verdict = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Cricket
        exclude = []

class footballform(ModelForm):
    preview = forms.CharField(widget=forms.Textarea)
    para1 = forms.CharField(widget=forms.Textarea)
    para2 = forms.CharField(widget=forms.Textarea)
    team1 = forms.CharField(widget=forms.Textarea)
    team2 = forms.CharField(widget=forms.Textarea)
    team3 = forms.CharField(widget=forms.Textarea)
    conclusion = forms.CharField(widget=forms.Textarea)
    final_verdict = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Football
        exclude = []

