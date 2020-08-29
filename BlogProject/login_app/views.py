from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserProfileChange, ProfilePicture, EditBio
# Create your views here.

def sign_up(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('login_app:login'))
        
    dict = {'form': form,}

    return render(request, 'login_app/signup.html', dict)

def login_page(request):
    form  = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
                
    
    return render(request, 'login_app/login.html', context={'form': form})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required 
def profile(request):
    return render(request, 'login_app/profile.html', {})

@login_required 
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/change_profile.html', {'form': form})

@login_required 
def pass_change(request):
    changed = False
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'login_app/change_password.html', {'form': form, 'changed': changed })

@login_required 
def add_profile_picture(request):
    form = ProfilePicture()
    if request.method == 'POST':
        form = ProfilePicture(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/add_profile_picture.html', {'form': form})

@login_required 
def change_profile_picture(request):
    form = ProfilePicture(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePicture(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/add_profile_picture.html', {'form': form, 'change': True})

@login_required 
def edit_bio(request):
    form = EditBio(instance=request.user.user_profile)
    if request.method == 'POST':
        form = EditBio(request.POST, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/edit_bio.html', {'form': form,})