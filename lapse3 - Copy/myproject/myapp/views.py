from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import UserProfile, UserContent
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
import json

def landing_page(request):
    # Clear session if user is accessing the landing page
    request.session.flush()
    return render(request, "myapp/landing_page.html")

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = UserProfile.objects.get(username=username)
            # Check if the password matches
            if check_password(password, user.password):
                # Set session variables
                request.session['logged_in'] = True
                request.session['username'] = username
                return JsonResponse({"success": True, "redirect_url": reverse("user_page", args=[username])})
            else:
                return JsonResponse({"success": False, "message": "Password is incorrect."})
        except UserProfile.DoesNotExist:
            # Create new user if username does not exist
            new_user = UserProfile(username=username, password=make_password(password))
            new_user.save()
            UserContent.objects.create(user=new_user, content="")
            request.session['logged_in'] = True
            request.session['username'] = username
            return JsonResponse({"success": True, "redirect_url": reverse("user_page", args=[username])})
    return JsonResponse({"success": False, "message": "Invalid request."})

@csrf_exempt
def save_content(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        content = data.get("content", "")

        # Check that user is logged in and session username matches
        if request.session.get('logged_in') and request.session.get('username') == username:
            user = get_object_or_404(UserProfile, username=username)
            user_content, _ = UserContent.objects.get_or_create(user=user)
            user_content.content = content
            user_content.save()
            return JsonResponse({"success": True, "message": "Content saved successfully!"})
        else:
            return JsonResponse({"success": False, "message": "Unauthorized access."})
    return JsonResponse({"success": False, "message": "Invalid request."})

def user_page(request, username):
    # Check if user is logged in and username matches session
    if request.session.get('logged_in') and request.session.get('username') == username:
        user = get_object_or_404(UserProfile, username=username)
        user_content, _ = UserContent.objects.get_or_create(user=user)
        return render(request, 'myapp/user_page.html', {'username': username, 'user_content': user_content})
    else:
        # Redirect to landing page if not logged in
        return redirect('landing_page')
