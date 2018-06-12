from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def home(request):
    username = 'stranger'
    if request.user.is_authenticated():
        username = request.user.username
    return render(request, 'home.html', { 'username': username })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('task_manager:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})