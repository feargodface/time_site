from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'time_site/home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/auth/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/auth/register.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
        'role': user.role,
        'post': user.post,
        'description': user.descripion
    }
    return render(request, 'accounts/profile/view.html', context)