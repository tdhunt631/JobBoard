from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ModelForm
from board.models import *
from django.template import RequestContext


def index(request):
	hello = "hello"
	context = {
		'hello': hello,
	}
	return render(request, 'board/index.html', context)

