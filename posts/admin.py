from django.contrib import admin

# Register your models here.

from .models import tag, post

admin.site.register(tag)
admin.site.register(post)
