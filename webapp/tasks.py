import datetime
import time
from webapp.models import Task
from celery import task
from webapp.choices import *
import findspark

findspark.init()
from pyspark import SparkContext
import math


@task()
def compute(task_to_do):
    if task_to_do.state == CANCELLED_STATUS:
        return 0

    start = time.time()
    result = ""
    task_to_do.state = WORKING_STATUS
    task_to_do.progress = 10
    task_to_do.save()

    sc = SparkContext(master="spark://10.0.75.1:7077", appName="Factorer")
    partitions = 2  # number from lecture
    main_number = int(task_to_do.number)  # getting number from task
    factorized = []
    x = number = main_number
    progress = 0

    while x > 1:
        sqrted = math.sqrt(number)
        rdd = sc.parallelize(range(2, int(round(sqrted + 1))), partitions)
        try:
            x = rdd.filter(lambda x: (number % x == 0)).first()
        except ValueError:
            x = 1

        if x > 1:
            number /= x
            progress += number
            task_to_do.progress = progress / main_number * 100
            task_to_do.save()
            factorized.append(x)
        else:
            factorized.append(number)

    if len(factorized) == 1:
        result = "Given number is prime."
    else:
        for fac in factorized:
            result += str(fac) + " * "

    sc.stop()

    task_to_do.state = DONE_STATUS
    task_to_do.progress = 100
    task_to_do.result = result[:-5]
    task_to_do.job_finished_date = datetime.datetime.now()
    end = time.time()
    task_to_do.time = end - start
    task_to_do.save()
    return 0


@task()
def schedule_task():
    task_in_progress = Task.objects.filter(state=WORKING_STATUS)
    if task_in_progress:
        return 0
    next_task = Task.objects.order_by("-priority", "job_date")
    print("Found task(priority): " + next_task.priority)
    compute.delay(next_task);
    print("Putted new task into queue.")
    return 0
