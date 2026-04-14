from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import UserRegisterForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                request.session['access_token'] = str(refresh.access_token)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})