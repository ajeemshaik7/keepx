# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),  # Landing page
    path("login-user/", views.login_user, name="login_user"),  # User login
    path("save_content/", views.save_content, name="save_content"),  # Save user content
    path("<str:username>/", views.user_page, name="user_page"),  # User-specific pages
]
