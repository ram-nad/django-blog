from django.db import models
from django.utils import timezone
from user.models import customuser

# Create your models here.

class tag(models.Model):
	first_name = models.CharField(max_length=50,primary_key=True)
	
	def __str__(self):
		return (self.first_name)
	def newinstance(self,name):
		self.first_name = name
		return self

class post(models.Model):
	title = models.CharField(max_length=50)
	creator = models.ForeignKey(customuser, on_delete=models.CASCADE)
	content = models.TextField()
	tags = models.ManyToManyField(tag)
	
	def __str__(self):
		return (self.title+" - "+self.creator.user.username)
	def newinstance(self,user,head,blog):
		self.title = head
		self.creator = user
		self.content = blog
		return self
