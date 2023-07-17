from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserProfileSerializer
from .models import UserProfile


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        
        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Save additional user details
        user_profile = UserProfile(user=user, mobile_number=mobile_number)
        user_profile.save()
        
        return redirect('login')
    
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log in the user
            login(request, user)
            return redirect('users')
    
    return render(request, 'login.html')

@login_required
def users(request):
    # Fetch all users from the database
    user_profiles = UserProfile.objects.all()
    
    return render(request, 'users.html', {'user_profiles': user_profiles})

@login_required
def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        
        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Save additional user details
        user_profile = UserProfile(user=user, mobile_number=mobile_number)
        user_profile.save()
        
        return redirect('users')
    
    return render(request, 'create_user.html')

@login_required
def edit_user(request, user_id):
    user_profile = UserProfile.objects.get(id=user_id)
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        
        # Update the user and user profile
        user_profile.user.username = username
        user_profile.user.email = email
        user_profile.mobile_number = mobile_number
        
        user_profile.user.save()
        user_profile.save()
        
        return redirect('users')
    
    return render(request, 'edit_user.html', {'user_profile': user_profile})

@login_required
def delete_user(request, user_id):
    user_profile = UserProfile.objects.get(id=user_id)
    
    if request.method == 'POST':
        # Delete the user and user profile
        user_profile.user.delete()
        user_profile.delete()
        
        return redirect('users')
    
    return render(request, 'delete_user.html', {'user_profile': user_profile})
