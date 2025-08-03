from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, CompanyRegistrationForm, UserLoginForm, ProfileUpdateForm
from .models import User



def home(request):
    return render(request, 'accounts/home.html')
# ---------------------------
# REGISTER STUDENT
# ---------------------------
def register_student(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'student'
            user.save()
            messages.success(request, "Your student account has been created. You can now log in.")
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register_student.html', {'form': form})


# ---------------------------
# REGISTER COMPANY
# ---------------------------
def register_company(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'company'
            user.save()
            messages.success(request, "Your company account has been created. You can now log in.")
            return redirect('login')
    else:
        form = CompanyRegistrationForm()

    return render(request, 'accounts/register_company.html', {'form': form})


# ---------------------------
# LOGIN VIEW
# ---------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back {user.username}!")
                return redirect('dashboard_redirect')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# ---------------------------
# LOGOUT VIEW
# ---------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


# ---------------------------
# DASHBOARD REDIRECT
# ---------------------------
@login_required
def dashboard_redirect(request):
    if request.user.user_type == 'student':
        return redirect('student_dashboard')
    elif request.user.user_type == 'company':
        return redirect('company_dashboard')
    return redirect('home')


# ---------------------------
# PROFILE VIEW
# ---------------------------
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


# ---------------------------
# EDIT PROFILE
# ---------------------------
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})
