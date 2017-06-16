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
from .choices import *

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
            priority = task_form_post.cleaned_data["priority"]
            task = Task(number=number, priority=priority, user=request.user)
            task.save()
            some_task.delay(task)
            tasks = Task.objects.filter(user=request.user).order_by("-job_date")
            return render(request, "dashboard.html",
                          dict(addedSuccessfully=True, task_form=task_form, tasks=tasks))
        else:
            return HttpResponse("Failed to get brute force number")
    else:
        tasks = Task.objects.filter(user=request.user).order_by("-job_date")
        return render(request, "dashboard.html", dict(task_form=task_form, tasks=tasks))


@login_required
def progress(request, task_id):
    task_in_progress = Task.objects.get(pk=task_id)
    return render(request, "progress.html", dict(task=task_in_progress))


@require_POST
@login_required
def progress_ajax(request):
    data_dict = json.loads(request.body.decode("utf-8"))
    task_progress = Task.objects.get(pk=data_dict["id"]).progress
    dict_to_return = dict(progress=task_progress)
    return HttpResponse(json.dumps(dict_to_return), content_type="application/json")


@require_POST
@login_required
def cancel_task_ajax(request):
    data_dict = json.loads(request.body.decode("utf-8"))
    task_to_cancel = Task.objects.get(pk=data_dict["id"])
    task_to_cancel.state = CANCELLED_STATUS
    task_to_cancel.save()
    dict_to_return = {"success": True}
    return HttpResponse(json.dumps(dict_to_return), content_type="application/json")


@staff_member_required
def users(request):
    all_users = User.objects.exclude(username="admin").order_by("username")
    return render(request, "users.html", dict(users=all_users))


@staff_member_required
def tasks(request):
    all_tasks = Task.objects.order_by("-job_date")
    return render(request,
                  "tasks.html",
                  dict(tasks=all_tasks))


@login_required
def edit_user(request, user_id):
    if request.method == "POST":
        # TODO edit of user
        all_users = User.objects.order_by("username")
        return render(request,
                      next,
                      dict(users=all_users))
    else:
        user = User.objects.get(pk=user_id)
        return render(request,
                      "edit_user.html",
                      dict(user=user))


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        # TODO edit of task
        tasks = Task.objects.order_by("job_date")
        return render(request,
                      "tasks.html",
                      dict(tasks=tasks))
    else:
        task_to_edit = Task.objects.get(pk=task_id)
        return render(request,
                      "edit_task.html",
                      dict(task=task_to_edit))


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"],
                                password=cd["password"])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    tasks = Task.objects.filter(user=request.user).order_by("-job_date")
                    return render(request, "dashboard.html",
                                  dict(loggedInSuccess=True, task_form=task_form, tasks=tasks))
            else:
                return render(request, "account/login.html", dict(form=login_form, disabled=True))
        else:
            return render(request, "account/login.html", dict(form=login_form))
    else:
        return render(request, "account/login.html", dict(form=login_form))


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
        return render(request,
                      "account/login.html",
                      dict(form=login_form, registrationSuccess=True))
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  "account/register.html",
                  dict(user_form=user_form))


@login_required
def logout(request):
    auth_logout(request)
    return render(request,
                  "account/login.html",
                  dict(form=login_form, loggedOut=True))


@staff_member_required
def delete_user_ajax(request):
    data_dict = json.loads(request.body.decode("utf-8"))
    user_to_delete = User.objects.get(pk=data_dict["id"])
    user_to_delete.delete()
    dict_to_return = {"success": True}
    return HttpResponse(json.dumps(dict_to_return), content_type="application/json")


@staff_member_required
def delete_task_ajax(request):
    data_dict = json.loads(request.body.decode("utf-8"))
    task_to_delete = Task.objects.get(pk=data_dict["id"])
    task_to_delete.delete()
    dict_to_return = {"success": True}
    return HttpResponse(json.dumps(dict_to_return), content_type="application/json")
