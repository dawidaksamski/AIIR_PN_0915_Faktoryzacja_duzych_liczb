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
LOW = 0
MEDIUM = 1
HIGH = 2
URGENT = 3
PRIORITY_CHOICES = (
    (LOW, "Low"),
    (MEDIUM, "Medium"),
    (HIGH, "High"),
    (URGENT, "Urgent")
)
