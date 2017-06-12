from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    CANCELLED_STATUS = -1
    WAITING = 0
    WORKING_STATUS = 1
    DONE_STATUS = 2
    STATUS_CHOICES = (
        (CANCELLED_STATUS, "Cancelled"),
        (WAITING, "Waiting"),
        (WORKING_STATUS, "Working"),
        (DONE_STATUS, "Done")
    )

    number = models.CharField(max_length=200)
    job_date = models.DateTimeField(default=timezone.now)
    job_finished_date = models.DateTimeField(null=True)
    state = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)
    priority = models.IntegerField(default=0)
    result = models.CharField(max_length=200)
    progress = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
