from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm, LoginForm, UsernameResetForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

# Signup view
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # Create profile automatically
            Profile.objects.get_or_create(user=user)

            login(request, user)
            return redirect('accounts:profile')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

# Username reset view
def username_reset_view(request):
    if request.method == "POST":
        form = UsernameResetForm(request.POST)
        if form.is_valid():
            return redirect('accounts:signup')
    else:
        form = UsernameResetForm()
    return render(request, 'accounts/username_reset.html', {'form': form})
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'bio': ''}
    )
    return render(request, 'accounts/profile.html', {'profile': profile})


    return render(request, 'accounts/profile.html', {'profile': profile})
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})
