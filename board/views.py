from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ModelForm
from board.models import *
from django.template import RequestContext
from django.contrib import messages

def index(request):
	if request.user.is_authenticated():
		try:
			profile = Profile.objects.get(user__username=request.user)
		except:
			return HttpResponseRedirect(reverse('board:createProfile'))

	hello = "hello"
	context = {
		'hello': hello,
	}
	return render(request, 'board/index.html', context)

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
			return HttpResponseRedirect('/post/')

		else:
			form = CreateProfileForm()		
			context = {
				'form': form,
			}
			return render(request, 'board/createProfile.html', context)

@login_required
def post(request):
			
	hello = "post new job page"
	context = {
		'hello': hello,
	}
	return render(request, 'board/post.html', context)

@login_required
def myPosts(request):

	hello = "my posts"
	context = {
		'hello': hello,
	}
	return render(request, 'board/myPosts.html', context)

def subscribe(request):
	return HttpResponseRedirect('/')

def unsubscribe(request):
	return HttpResponseRedirect('/')


