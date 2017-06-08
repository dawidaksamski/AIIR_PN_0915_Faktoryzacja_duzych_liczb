from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm


login_form = LoginForm


def index_view(request):
    return render(request, "index.html")


def logout(request):
    auth_logout(request)
    return render(request,
                  "account/login.html",
                  {"form": login_form, "loggedOut": True})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return render(request, "index.html", {"loggedInSuccess": True})
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        return render(request, 'account/login.html', {'form': login_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
        return render(request,
                      'account/login.html',
                      {'form': login_form, "registrationSuccess": True})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})
