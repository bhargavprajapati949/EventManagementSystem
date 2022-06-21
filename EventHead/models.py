from django.db import models
from UserManager.models import Event_Committee
from EventWebSite.models import Event, Participation
# Create your models here.

class Event_Head(models.Model):
    reg_no = models.ForeignKey(Event_Committee, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    isActive = models.BooleanField(default = False)

    def __str__(self):
        return super().__str__()

class Winner(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    winner = models.ForeignKey(Participation, on_delete = models.SET_DEFAULT, default = 0)
    allowed_positions = [
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third')
    ]
    position = models.IntegerField(choices = allowed_positions)
    winning_certificate_issue = models.BooleanField(default = False)
    winning_certi_otp = models.IntegerField()
    event_head = models.ForeignKey(Event_Head, null=True, on_delete = models.SET_NULL)

    def __str__(self):
        str = self.position + " in " + self.event + " " + self.winner
        return str