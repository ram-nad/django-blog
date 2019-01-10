from django.urls import path
from . import views

urlpatterns = [
	path('',views.index),
	path('register',views.register,name='register'),
	path('login',views.log_in,name='login'),
	path('logout',views.log_out,name='logout'),
	path('update',views.update,name='update'),
	path('create',views.create,name='create'),
	path('explore',views.explore,name='explore'),
]
