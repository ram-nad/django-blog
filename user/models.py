from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class customuser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.SlugField()
	bio = models.TextField()
	bdate = models.DateField()
	
	def __str__(self):
		return (self.name+"@"+self.user.username)
	
	def newinstance(self,us,na,bi,bd):
		self.user = us
		self.name = na
		self.bio = bi
		self.bdate = bd
		return self
	def recentpost(self):
		return self.post_set.all().order_by("-pk").first()

