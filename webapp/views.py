import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import LoginForm, UserRegistrationForm, TaskForm
from .models import Task
from .tasks import some_task

login_form = LoginForm
task_form = TaskForm


def index(request):
    return render(request, "index.html")


@login_required
def dashboard(request):
    if request.method == "POST":
        task_form_post = TaskForm(request.POST)
        if task_form_post.is_valid():
            number = task_form_post.cleaned_data["number"]
            task = Task(number=number, user=request.user)
            task.state = Task.WAITING
            task.save()
            some_task.delay(task)
            tasks = Task.objects.filter(user=request.user).order_by("-job_date")
            return render(request, "dashboard.html", {"addedSuccessfully": True,
                                                      "task_form": task_form,
                                                      "tasks": tasks})
        else:
            return HttpResponse("Failed to get brute force number")
    else:
        tasks = Task.objects.filter(user=request.user).order_by("-job_date")
        return render(request, "dashboard.html", {"task_form": task_form,
                                                  "tasks": tasks})


@login_required
def progress(request, task_id):
    task_in_progress = Task.objects.get(pk=task_id)
    return render(request, "progress.html", {"task": task_in_progress})


@require_POST
@login_required
def progress_ajax(request):
    data_dict = json.loads(request.body.decode("utf-8"))
    task_progress = Task.objects.get(pk=data_dict["id"]).progress
    dict_to_return = {"progress": task_progress}
    return HttpResponse(json.dumps(dict_to_return), content_type='application/json')


@staff_member_required
def users(request):
    users = User.objects.order_by("username")
    return render(request, "users.html", {"users": users})


@login_required
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
                    tasks = Task.objects.filter(user=request.user).order_by("-job_date")
                    return render(request, "dashboard.html", {"loggedInSuccess": True,
                                                              "task_form": task_form,
                                                              "tasks": tasks})
            else:
                return render(request, 'account/login.html', {'form': login_form,
                                                              "disabled": True})
        else:
            return render(request, 'account/login.html', {'form': login_form})
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
