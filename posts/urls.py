from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name='home'),
	path('#<str:name>',views.tagspage,name='tags'),
	path('<str:name>',views.mainpage,name='index'),
	path('<str:name>/<int:postkey>',views.postview,name='postview')
]
