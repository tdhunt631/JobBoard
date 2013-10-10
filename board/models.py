from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, ModelChoiceField
from sorl.thumbnail import ImageField
from django_summernote.widgets import SummernoteWidget

class Profile(models.Model):
	user = models.ForeignKey(User)
	companyName = models.CharField(max_length=100)
	description = models.TextField()  #using django-summernote
	website = models.CharField(max_length=100)
	contactName = models.CharField(max_length=50)
	contactEmail = models.CharField(max_length=50)
	logo = ImageField(upload_to='media/logos/', blank=True, null=True)

	def __unicode__(self):
		return self.companyName	

class Subscribe(models.Model):
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	active = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.name

class JobType(models.Model):
	title = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.title

class Post(models.Model):
	profile = models.ForeignKey(Profile)
	title = models.CharField(max_length=100)
	description = models.TextField()  #using django-summernote
	jobType = models.ForeignKey(JobType)
	wage = models.CharField(max_length=20, blank=True, null=True)
	publishDate = models.DateTimeField(auto_now_add=True)
	expirationDate = models.DateTimeField()
	active = models.BooleanField(default=True)
	views = models.IntegerField(default=0)

	def __unicode__(self):
		return self.title
	
	
