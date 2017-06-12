"""Factorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from webapp import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^admin/", admin.site.urls),
    url(r"^login/?$", views.login, name="login"),
    url(r"^register/?$", views.register, name="register"),
    url(r"^logout/?$", views.logout, name="logout"),
    url(r"^dashboard/?$", views.dashboard, name="dashboard"),
    url(r"^users/?$", views.users, name="users"),
    url(r"^progress/(?P<task_id>\d+)/?$", views.progress, name="progress"),
    url(r"^progress/progress-ajax/?$", views.progress_ajax, name="progress-ajax")
]
