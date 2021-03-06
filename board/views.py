from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ModelForm
from board.models import *
from django.template import RequestContext
from django.contrib import messages
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

def sendMail(subscribers, post):
	emails = []
	for subscriber in subscribers:
		emails.append(subscriber.email)
	send_mail('A new job has been posted!',
	get_template('board/email.html').render(
		Context({'post': post,})
	), 'jobboarddixie@gmail.com', emails, fail_silently=False)
	
def index(request):
	#redirect newly registered users to the profile page.
	if request.user.is_authenticated():
		try:
			profile = Profile.objects.get(user__username=request.user)
		except:
			return HttpResponseRedirect(reverse('board:createProfile'))
	
	#get all active jobs that aren't expired
	posts = Post.objects.filter(active=True).exclude(expirationDate__lte=datetime.date.today()).order_by('-publishDate')[:30]
	context = {
		'posts': posts,
	}
	return render(request, 'board/index.html', context)

def detail(request, post_id):
	try:
		post = get_object_or_404(Post, id=post_id)
		if post.active == True and post.expirationDate >= timezone.now():
			#increment the number of times the job has been viewed
			post.views += 1
			post.save()
			context = {
				'post': post,
			}
			return render(request, 'board/detail.html', context)		
		messages.add_message(request, messages.SUCCESS, "Sorry, the job post was not found, or the job has expired.")
		return HttpResponseRedirect(reverse('board:index'))
	except:
		messages.add_message(request, messages.SUCCESS, "Sorry, the job post was not found.")
		return HttpResponseRedirect(reverse('board:index'))

@login_required
def profile(request):
	if request.method == 'POST':
		user = get_object_or_404(User, id=request.user.id)
		profile = get_object_or_404(Profile, user=request.user.id)
		data = CreateProfileForm(request.POST, request.FILES, instance=profile)
		form = data.save(commit=False)
		form.user = user
		form.save()
		messages.add_message(request, messages.SUCCESS, "Your profile has been updated.")
		return HttpResponseRedirect('/')

	else:
		profile = get_object_or_404(Profile, user=request.user.id)
		form = CreateProfileForm(instance=profile)
		context = {
			'form': form,
			'profile': profile,
		}
		return render(request, 'board/profile.html', context)

@login_required
def createProfile(request):
	try:
		profile = get_object_or_404(Profile, user=request.user.id)
		return HttpResponseRedirect('/profile/')

	except:
		if request.method == 'POST':
			user = get_object_or_404(User, id=request.user.id)
			data = CreateProfileForm(request.POST, request.FILES)
			form = data.save(commit=False)
			form.user = user
			form.save()
			messages.add_message(request, messages.SUCCESS, "Your profile has been created. You may now post your job.")
			return HttpResponseRedirect('/post/')

		else:
			form = CreateProfileForm()		
			context = {
				'form': form,
			}
			return render(request, 'board/createProfile.html', context)

@login_required
def myPosts(request):
	profile = get_object_or_404(Profile, user=request.user.id)
	jobs = Post.objects.filter(profile=profile).order_by('-publishDate')
	context = {
		'jobs': jobs,
	}
	return render(request, 'board/myPosts.html', context)

@login_required
def post(request):
	if request.method == 'POST':
		profile = get_object_or_404(Profile, user=request.user.id)
		data = PostForm(request.POST)
		form = data.save(commit=False)
		form.profile = profile
		form.save()
		# send email to notify subscribers
		subscribers = Subscribe.objects.all()
		if form.active == True:
			sendMail(subscribers, form)
		messages.add_message(request, messages.SUCCESS, "Thanks.  Your job has been posted successfully.")
		return HttpResponseRedirect('/myPosts/')

	else:
		form = PostForm()
		context = {
			'form': form,
		}
		return render(request, 'board/post.html', context)

@login_required
def editPost(request, post_id):
	profile = get_object_or_404(Profile, id=request.user.id)
	post = get_object_or_404(Post, id=post_id)
	if post.profile != profile:
		messages.add_message(request, messages.SUCCESS, "This job does not belong to you. Please select a job from the list below.")
		return HttpResponseRedirect('/myPosts/')

	if request.method == 'POST':
		data = PostForm(request.POST, instance=post)
		form = data.save(commit=False)
		form.profile = profile
		form.save()
		messages.add_message(request, messages.SUCCESS, "Your job post has been updated successfully.")
		return HttpResponseRedirect('/myPosts/')
	else:
		form = PostForm(instance=post)
		context = {
			'form': form,
			'post': post,
		}
		return render(request, 'board/editPost.html', context)				

def subscribe(request):
	if request.method == 'POST':
		form = SubscribeForm(request.POST)
		form.save()
		messages.add_message(request, messages.SUCCESS, "Thanks! You will now be notified of new job posts.")
		return HttpResponseRedirect(reverse('board:index'))
	else:
		form = SubscribeForm()
		context = {
			'form': form,
		}
	return render(request, 'board/subscribe.html', context)

def unsubscribe(request):
	if request.method == 'POST':
		subscriber = request.POST.get('email')
		email = Subscribe.objects.filter(email=subscriber).delete()
		messages.add_message(request, messages.SUCCESS, "Success! You will no longer be notified of new job posts.")
		return HttpResponseRedirect(reverse('board:index'))
	else:
		form = UnsubscribeForm()
		context = {
			'form': form,
		}
		return render(request, 'board/unsubscribe.html', context)
	

