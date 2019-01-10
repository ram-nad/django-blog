from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import customuser
from django.http import HttpResponseNotFound, HttpResponseRedirect
from datetime import datetime, timedelta
from posts.models import post, tag

# Create your views here.

def register(request):
	if request.method == 'POST':
		try:
			uname = request.POST['username']
			passw1 = request.POST['password1']
			passw2 = request.POST['password2']
			name = request.POST['name']
			bio = request.POST['about']
			birth = request.POST['date']
		except KeyError:
			return render(request,'user/reg.html',{'nodata':"Enter Data Correctly"})
		error_messages = {}
		if not uname.isalnum() or not uname[0].isalpha():
			error_messages.update({'username':"Should start with alphabet and be alphanumeric"})
		elif User.objects.filter(username=uname).count() > 0 or uname=="user":
			error_messages.update({'username':"Username already exists"})
		else:
			pass
		if passw1 == "":
			error_messages.update({'password':"Password cannot be empty"})
		elif passw2 == "":
			error_messages.update({'password':"Enter both Password fields"})
		elif passw1 != passw2:
			error_messages.update({'password':"Password Fields do not match"})
		else:
			pass
		try:
			birthdate = datetime.strptime(birth, "%Y-%m-%d")
			if (birthdate > (datetime.now() - timedelta(days=4382))):
				error_messages.update({'date':"Date must be valid"})
			else:
				pass
		except ValueError:
			error_messages.update({'date':"Date must be valid"})
		if name == "":
			error_messages.update({'name':"Name cannot be empty"})
		if error_messages:
			return render(request,'user/reg.html',error_messages)
		else:
			user = User.objects.create_user(username=uname,password=passw1)
			new = customuser()
			new = customuser.newinstance(new,user,name,bio,birthdate)
			new.save()
			login(request,user)
			return HttpResponseRedirect(reverse('index', args=(new.user.username,)))
	else:
		return render(request,'user/reg.html')

def log_in(request):
	if request.user.is_authenticated and not request.user.is_staff:
		return HttpResponseRedirect(reverse('index', args=(request.user.username,)))
	elif request.user.is_authenticated:
		logout(request)
		return HttpResponseRedirect(reverse('login', args=()))
	else:
		if request.method == 'POST':
			try:
				uname = request.POST['username']
				passw = request.POST['password']
				user = authenticate(request, username=uname, password=passw)
				if user is not None and not user.is_staff:
					login(request,user)
					return HttpResponseRedirect(reverse('index', args=(user.username,)))
				else:
					return render(request,'user/login.html',{'error':'Wrong Login Credentials'})
			except KeyError:
				return HttpResponseRedirect(reverse('login', args=()))
		else:
			return render(request,'user/login.html')

def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('home', args=()))

def index(request):
	return HttpResponseRedirect(reverse('home', args=()))

def update(request):
	if request.user.is_authenticated and not request.user.is_staff:
		if request.method == 'POST':
			try:
				passw1 = request.POST['password1']
				passw2 = request.POST['password2']
				passo = request.POST['oldpass']
				name = request.POST['name']
				bio = request.POST['about']
				error_messages = {}
				if passw1 and passw2 and passw1 != passw2:
					error_messages.update({'password':"Password Fields do not match"})
				if name == "":
					error_messages.update({'name':"Name cannot be empty"})
				if error_messages:
					error_messages.update({'namedata':name,'bio':bio})
					return render(request,'user/update.html',error_messages)
				elif not request.user.check_password(passo):
					return render(request,'user/update.html',{'nodata':"Old Pasword not Correct",'bio':bio, 'namedata':name})
				else:
					if passw1 and passw2 and passw1==passw2:
						user = request.user
						user.set_password(passw1)
						user.save()
						update_session_auth_hash(request,request.user)
					new = request.user.customuser
					new.name = name
					new.bio = bio
					new.save()
					return HttpResponseRedirect(reverse('index', args=(request.user.username,)))
			except KeyError:
				return render(request,'user/update.html',{'nodata':"Enter Data Correctly",'bio':request.user.customuser.bio, 'namedata':request.user.customuser.name})
		else:
			return render(request,'user/update.html', {'bio':request.user.customuser.bio, 'namedata':request.user.customuser.name})
	elif request.user.is_authenticated:
		logout(request)
		return HttpResponseRedirect(reverse('login', args=()))
	else:
		return HttpResponseRedirect(reverse('login', args=()))


def create(request):
	if request.user.is_authenticated and not request.user.is_staff:
		if request.method == 'POST':
			try:
				tags = request.POST['tags']
				title = request.POST['title']
				blog = request.POST['blog']
				error_messages = {}
				if title == "":
					error_messages.update({'title':"Title cannot be empty"})
				if blog == "":
					error_messages.update({'blog':"Blog cannot be empty"})
				for a_tag in tags.split(','):
					if not a_tag.isalpha() or not a_tag:
						error_messages.update({'tags':"Tags need to be plain word seprated by comma"})
				if error_messages:
					error_messages.update({'titledata':title,'blogdata':blog,'tagsdata':tags})
					return render(request,'user/create.html',error_messages)
				else:
					tagslist = []
					for a_tag in tags.split(','):
						try:
							tagins = tag.objects.get(first_name=a_tag)
						except tag.DoesNotExist:
							tagins = tag()
							tagins = tag.newinstance(tagins,a_tag)
							tagins.save()
					postins = post()
					postins = post.newinstance(postins,request.user.customuser,title,blog)
					postins.save()
					for a_tag in tags.split(','):
						postins.tags.add(tag.objects.get(first_name=a_tag))
					return HttpResponseRedirect(reverse('postview', args=(request.user.username,postins.pk)))
			except KeyError:
				return render(request,'user/create.html',{'nodata':"Enter Data Correctly"})
		else:
			return render(request,'user/create.html', {})
	elif request.user.is_authenticated:
		logout(request)
		return HttpResponseRedirect(reverse('login', args=()))
	else:
		return HttpResponseRedirect(reverse('login', args=()))

def explore(request):
	if request.user.is_authenticated:
		persons = customuser.objects.exclude(user=request.user).exclude(post=None).order_by('?')[:5]
	else:
		persons = customuser.objects.exclude(post=None).order_by('?')[:5]
	return render(request,'user/explore.html',{'persons':persons})
