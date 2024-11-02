from django.contrib import admin

from .models import UserContent, UserProfile

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserContent)