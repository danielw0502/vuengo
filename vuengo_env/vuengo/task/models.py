from django.db import models

# Create your models here.
class Task(models.Model):
    TODO = 0
    DONE = 1

    STATUS_CHOICES = (
        (TODO,'To do'),
        (DONE, 'Done')
    )

    description = models.CharField(max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES,default=TODO)
    editing = models.BooleanField(default=False)
    beforeEditCache = models.CharField(max_length=255,default='')