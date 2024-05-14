from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_not_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm

from makemake.core.forms import LoginForm


def home(request):
    return render(request, 'core/index.html')

@login_not_required
def login_initial(request):
    if request.user.is_authenticated:
        return render(request, 'core/index.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm(request.POST)
            return render(request, 'core/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'core/login.html', {'form': form})


def logout_user(request):
    # Log out the user.
    # since function cannot be same as django method, esle it will turn into recursive calls
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('login'))

@login_not_required
def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = request.POST.get("password1", "")
            user.set_password(password) # Criptography password
            user.is_active=False
            user.is_staff=False
            user.is_superuser=False
            user.save()
            # message = "The admin will approve your access within 24 hours, please wait!"
            # messages.success(request, message)
            return redirect('login')
        else:
            message = "Please revise your credentials!"
            messages.error(request, message)

    context = {'form': form}

    return render(request, 'core/register.html', context)