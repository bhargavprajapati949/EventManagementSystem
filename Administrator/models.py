from django.db import models
from UserManager.models import User, Event_Committee
from EventWebSite.models import Participants
# Create your models here.

class Admin(models.Model):    
    reg_no = models.OneToOneField(Event_Committee, on_delete = models.CASCADE, primary_key = True)
    isActive = models.BooleanField(default = False)

    def __str__(self):
        return super().__str__()

# class to_whome_paid(models.Model):
#     reg_no = models.ForeignKey(Participants, on_delete = models.CASCADE)
#     to_paid = models.ForeignKey(User, on_delete = models.SET_DEFAULT, default = 0)
#     amount = models.IntegerField()
#     date_time = models.DateTimeField()

#     def __str__(self):
#         str = "Paid by " + self.reg_no + " to " + self.to_paid
#         return str

# class vol_to_admin_pay(models.Model):
#     reg_no = models.ForeignKey(Admin, on_delete = models.SET_DEFAULT, default = 0)
#     vol_id = models.ForeignKey(Event_Committee, on_delete = models.SET_DEFAULT, default = 0)
#     amount = models.IntegerField(default = 0)
#     date_time = models.DateTimeField()

#     def __str__(self):
#         str = "Paid by " + self.reg_no + " to " + self.vol_id
#         return str

class Payments(models.Model):
    payment_id = models.AutoField(primary_key = True, verbose_name = "Payment Id")
    reg_no = models.ForeignKey(Participants, on_delete = models.SET_DEFAULT, default = 0)
    amount = models.IntegerField(default = 0)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        str = "Paid by " + self.reg_no + " amount " + self.amount
        return str

class Sponsers(models.Model):
    s_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    logo = models.ImageField(upload_to = 'sponsers_logo')
    amount = models.IntegerField(null = True)
    done_by = models.ForeignKey(Event_Committee, on_delete = models.SET_DEFAULT, default = 0)
    date = models.DateField()

    def __str__(self):
        return self.name