from celery import task
import time, datetime


@task()
def some_task(task_to_do):
    task_to_do.state = task_to_do.WORKING_STATUS
    task_to_do.save()
    for i in range(1, 21):
        task_to_do.progress = i * 5
        task_to_do.save()
        time.sleep(1)

    task_to_do.state = task_to_do.DONE_STATUS
    task_to_do.result = "2x2x2x3x5x7x2x2x2x2x2x2x2"
    task_to_do.job_finished_date = datetime.datetime.now()
    task_to_do.save()
    return 0
