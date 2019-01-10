from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from .models import tag, post
from user.models import customuser
from django.contrib.auth.models import User

# Create your views here.

def mainpage(request, name):
	try:
		page = User.objects.get(username=name)
		posts = list(page.customuser.post_set.all())
		return render(request, 'posts/base.html', {'person' : page.customuser, 'posts':posts})
	except User.DoesNotExist:
		return HttpResponseNotFound("<html><head><title>Not Found</title></head><body><h1>The User does not exists.</h1></body></html>")

def tagspage(request, name):
	try:
		page = tag.objects.get(first_name=name)
		posts = list(page.post_set.all())
		if posts:
			return render(request, 'posts/tags.html', {'tag' : page, 'posts':posts})
		else:
			return HttpResponseNotFound("<html><head><title>Not Found</title></head><body><h1>There is no post with this tag.</h1></body></html>")
	except tag.DoesNotExist:
		return HttpResponseNotFound("<html><head><title>Not Found</title></head><body><h1>There is no post with this tag.</h1></body></html>")

def postview(request, name, postkey):
	try:
		page = User.objects.get(username=name)
		try:
			my_post = post.objects.get(pk=postkey)
			if my_post.creator.user == page:	
				return render(request, 'posts/full.html', {'post':my_post})
		except post.DoesNotExist:
			posts = list(page.customuser.post_set.all())
			return render(request, 'posts/base.html', {'person' : page.customuser, 'posts':posts})
	except User.DoesNotExist:
		return HttpResponseNotFound("<html><head><title>Not Found</title></head><body><h1>The User does not exists.</h1></body></html>")

def index(request):
	posts = post.objects.order_by("-pk")[:5]
	return render(request, 'posts/home.html', {'posts':posts})
