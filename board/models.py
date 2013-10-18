from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, ModelChoiceField
from sorl.thumbnail import ImageField
from django_summernote.widgets import SummernoteWidget

## MODELS ##

class Profile(models.Model):
	user = models.ForeignKey(User)
	companyName = models.CharField(max_length=100)
	description = models.TextField()  #using django-summernote
	website = models.CharField(max_length=100)
	contactName = models.CharField(max_length=50)
	contactEmail = models.CharField(max_length=50)
	logo = ImageField(upload_to='media/logos/', blank=True)

	def __unicode__(self):
		return self.companyName	

class Subscribe(models.Model):
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = 'Subscribers'

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
	
## FORMS ##

class CreateProfileForm(ModelForm):
	description = forms.CharField(widget=SummernoteWidget())  #replaced the TextArea widget

	class Meta:
		model = Profile
		fields = ['logo','companyName','description','website','contactName','contactEmail',]	
	
	def __init__(self, *args, **kwargs):
		super(CreateProfileForm, self).__init__(*args, **kwargs)
		self.fields['description'].label = "Company Description"
		self.fields['companyName'].label = "Company Name"
		self.fields['contactName'].label = "Contact Name"
		self.fields['contactEmail'].label = "Contact Email"

class PostForm(ModelForm):
	description = forms.CharField(widget=SummernoteWidget())  #replaced the TextArea widget

	class Meta:
		model = Post
		fields = ['title','description','jobType','wage','expirationDate', 'active',]	
	
	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['title'].label = "Job Title"
		self.fields['description'].label = "Job Description"
		self.fields['jobType'].label = "Job Type"
		self.fields['expirationDate'].label = "Expiration Date"
		self.fields['active'].label = "Currently Active?"

class SubscribeForm(ModelForm):
	class Meta:
		model = Subscribe

class UnsubscribeForm(ModelForm):
	class Meta:
		model = Subscribe
		fields = ['email',]
		
