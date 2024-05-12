from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

from makemake.core.forms import LoginForm

# Create your views here.
def home(request):
    return render(request, 'index.html')

# Create your views here.
def login1(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
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
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
