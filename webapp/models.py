from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from webapp.choices import *


class Task(models.Model):
    number = models.CharField(max_length=200)
    job_date = models.DateTimeField(default=timezone.now)
    job_finished_date = models.DateTimeField(null=True)
    state = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=LOW)
    result = models.CharField(max_length=200)
    progress = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)

    def __str__(self):
        return str(self.number)
