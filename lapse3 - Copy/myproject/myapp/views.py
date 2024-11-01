from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import UserProfile, UserContent
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
import json

def landing_page(request):
    return render(request, "myapp/landing_page.html")

@csrf_exempt  # Exempt CSRF for AJAX POST
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = UserProfile.objects.get(username=username)
            # Check if the password matches
            if check_password(password, user.password):
                # User exists and password is correct, set session variable
                request.session['logged_in'] = True  # Indicate login status
                request.session['username'] = username  # Store username in session
                return JsonResponse({"success": True, "redirect_url": reverse("user_page", args=[username])})
            else:
                # Password is incorrect
                return JsonResponse({"success": False, "message": "Password is incorrect or create a new username."})

        except UserProfile.DoesNotExist:
            # Create a new user if the username does not exist
            new_user = UserProfile(username=username, password=make_password(password))
            new_user.save()
            # Create content for new user
            UserContent.objects.create(user=new_user, content="")  # Start with empty content
            
            # Set session variables for new user login
            request.session['logged_in'] = True
            request.session['username'] = username
            return JsonResponse({"success": True, "redirect_url": reverse("user_page", args=[username])})
    return JsonResponse({"success": False, "message": "Invalid request."})


@csrf_exempt
def save_content(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Parse JSON data from request body
        username = data.get("username")
        content = data.get("content", "")  # Get the content

        # Get the user profile
        user = get_object_or_404(UserProfile, username=username)
        
        # Get or create the UserContent object
        user_content, _ = UserContent.objects.get_or_create(user=user)
        user_content.content = content  # Save the content
        user_content.save()  # Save changes
        
        return JsonResponse({"success": True, "message": "Content saved successfully!"})
    return JsonResponse({"success": False, "message": "Invalid request."})


def user_page(request, username):
    # Check if user is logged in by verifying session variable
    if request.session.get('logged_in') and request.session.get('username') == username:
        user = get_object_or_404(UserProfile, username=username)
        user_content, _ = UserContent.objects.get_or_create(user=user)  # Get or create content for the user
        return render(request, 'myapp/user_page.html', {'username': username, 'user_content': user_content})
    else:
        # Redirect to landing page if not logged in
        return redirect('landing_page')

