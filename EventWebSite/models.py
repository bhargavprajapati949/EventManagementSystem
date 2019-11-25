from django.db import models
from UserManager.models import User, Event_Committee, Admin, Volunteer, Event_Head

# Create your models here.

# class Parent_event(models.Model):
#     parent_event_id = models.AutoField(primary_key = True)
#     parent_event_name = models.CharField(max_length = 50, unique = True)

class Event(models.Model):
    event_id = models.AutoField(primary_key = True)
    event_name = models.CharField(max_length = 50)
    event_detail = models.TextField()
    rules = models.TextField()
    event_logo = models.ImageField(upload_to = 'event_logo/', null=True)
    fees = models.IntegerField()
    event_statuses = [
        ('Available', 'Available'),
        ('Scrapped', 'Scrapped'),
        ('Delete', 'Delete'),
        ('Full', 'Full')
    ]
    event_status = models.CharField(max_length = 30, choices = event_statuses)    
    venue = models.CharField(max_length = 50)
    date_time = models.DateTimeField(blank = True)
    # parent_event = models.ForeignKey(Parent_event, on_delete = models.SET_DEFAULT, default = 0)

class news(models.Model):
    news_id = models.AutoField(primary_key = True)
    news_receivers = [
        ('Participants', 'Participants'),
        ('Volunteer', 'Volunteer')
    ]
    for_whome = models.CharField(max_length = 50, choices = news_receivers, verbose_name = 'News Viewers')
    news_content = models.CharField(max_length = 1000 ,verbose_name = 'News Content')
    hyperlink = models.CharField(verbose_name = 'hyperlink', max_length=50)


class Registers(models.Model):
    reg_no = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)
    remark = models.TextField(default = None, null=True)
    total_payment = models.IntegerField()
    remaining_payment = models.IntegerField()
    paid_payment = models.IntegerField(default = 0)
    filled_by = models.ForeignKey(Volunteer, null=True, on_delete = models.SET_NULL, default = None)
    # conformed = models.BooleanField(default = False)
    is_paid = models.BooleanField(default = False)

class Participation(models.Model):
    reg_no = models.ForeignKey(Registers, on_delete = models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete = models.SET_DEFAULT, default = 0)
    allowed_event_status = [
        ('Not_paid', 'Not Paid'),
        ('Paid', 'Paid'),
        ('Comform', 'Conform'), 
        ('Attended', 'Attended'),
        ('Certificate_issued', 'Certificate Issued'),
        ('Attended_winner', 'Attended Winner'),
        ('Scrapped', 'Scrapped'),
        ('Delete', 'Delete')
    ]
    reg_status = models.CharField(max_length = 50, choices = allowed_event_status)
    certi_otp = models.IntegerField()
    # event_attendance_qr = models.ImageField(upload_to = 'event_attendance_qr')
    amount = models.IntegerField()


class Winner(models.Model):
    event_id = models.ForeignKey(Event, on_delete = models.CASCADE)
    allowed_positions = [
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third')
    ]
    position = models.IntegerField(choices = allowed_positions)
    winner_reg_no = models.ForeignKey(Registers, on_delete = models.SET_DEFAULT, default = 0)
    winning_certificate_issue = models.BooleanField(default = False)
    certi_otp = models.IntegerField()
    event_head_id = models.ForeignKey(Event_Head, null=True, on_delete = models.SET_NULL)

class to_whome_paid(models.Model):
    reg_no = models.ForeignKey(Registers, on_delete = models.CASCADE)
    to_paid = models.ForeignKey(User, on_delete = models.SET_DEFAULT, default = 0)
    amount = models.IntegerField()
    date_time = models.DateTimeField()

class vol_to_admin_pay(models.Model):
    a_id = models.ForeignKey(Admin, on_delete = models.SET_DEFAULT, default = 0)
    vol_id = models.ForeignKey(Event_Committee, on_delete = models.SET_DEFAULT, default = 0)
    amount = models.IntegerField(default = 0)
    date_time = models.DateTimeField()

class Sponsers(models.Model):
    s_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    logo = models.ImageField(upload_to = 'sponsers_logo')
    amount = models.IntegerField(null = True)
    done_by = models.ForeignKey(Event_Committee, on_delete = models.SET_DEFAULT, default = 0)
    date = models.DateField()