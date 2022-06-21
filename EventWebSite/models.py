from django.db import models
from UserManager.models import User, Event_Committee


# Create your models here.

# class Parent_event(models.Model):
#     parent_event_id = models.AutoField(primary_key = True)
#     parent_event_name = models.CharField(max_length = 50, unique = True)

class Event(models.Model):
    event_id = models.AutoField(primary_key = True, verbose_name = "Event Id")
    event_name = models.CharField(max_length = 50, verbose_name = "Event Name")
    event_detail = models.TextField(verbose_name = "Event Details")
    rules = models.TextField(verbose_name = "Rules")
    event_logo = models.ImageField(upload_to = 'event_logo/', null=True, verbose_name = "Event Logo")
    fees = models.IntegerField(verbose_name = "Fees")
    event_statuses = [
        ('Available', 'Available'),
        ('Scrapped', 'Scrapped'),
        ('Delete', 'Delete'),
        ('Full', 'Full')
    ]
    event_status = models.CharField(max_length = 30, choices = event_statuses, verbose_name = "Event Status")
    venue = models.CharField(max_length = 50, verbose_name = "Venue", null=True)
    date_time = models.DateTimeField(blank = True, null=True, verbose_name = "Event Date & Time")
    # parent_event = models.ForeignKey(Parent_event, on_delete = models.SET_DEFAULT, default = 0)

    def __str__(self):
        return self.event_name

class news(models.Model):
    news_id = models.AutoField(primary_key = True)
    news_content = models.CharField(max_length = 1000 ,verbose_name = 'News Content')
    hyperlink = models.CharField(verbose_name = 'hyperlink', max_length=50)

    def __str__(self):
        return self.news_content
    
class Participants(models.Model):
    reg_no = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)
    remark = models.TextField(default = None, null=True)
    total_payment = models.IntegerField()
    remaining_payment = models.IntegerField()
    paid_payment = models.IntegerField(default = 0)
    # filled_by = models.ForeignKey(Volunteer, null=True, on_delete = models.SET_NULL, default = None)
    # conformed = models.BooleanField(default = False)
    is_paid = models.BooleanField(default = False)

    def __str__(self):
        return super().__str__()

class Participation(models.Model):
    reg_no = models.ForeignKey(Participants, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.SET_DEFAULT, default = 0)
    allowed_event_status = [
        ('Not Paid', 'Not Paid'),
        ('Paid', 'Paid'),
        ('Confirm', 'Confirm'), 
        ('Attended', 'Attended'),
        ('Attended Winner', 'Attended Winner'),
        ('Certificate Issued', 'Certificate Issued'),
        ('Winner Certificate Issued', 'Winner Certificate Issued'),
        ('Scrapped', 'Scrapped'),
        ('Delete', 'Delete')
    ]
    reg_status = models.CharField(max_length = 50, choices = allowed_event_status)
    certi_otp = models.IntegerField()
    attendance_otp = models.IntegerField()
    # event_attendance_qr = models.ImageField(upload_to = 'event_attendance_qr')

    # def __str__(self):
    #     str = self.reg_no + " Participated in " + self.event
    #     return str