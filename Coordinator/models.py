from operator import mod
from django.db import models
from UserManager.models import Event_Committee

# Create your models here.
class Coordinator(models.Model):
    reg_no = models.OneToOneField(Event_Committee, on_delete = models.CASCADE, primary_key=True)
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return super().__str__()