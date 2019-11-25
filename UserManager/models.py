from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Collages(models.Model):
    clg_id = models.CharField(max_length = 4, unique=True)
    clg_name = models.CharField(max_length = 100)

    def __str__(self):
        return self.clg_name

class Stream(models.Model):
    stream_id = models.CharField(max_length = 5, unique=True)
    stream_name = models.CharField(max_length = 100)

    def __str__(self):
        return self.stream_name

class UserManager(BaseUserManager):
    def _create_user(self, fname, lname, contect_no, email, password=None):
    
        user=self.model(
            fname = fname,
            lname = lname,
            contect_no = contect_no,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        return user

    def create_user(self, fname, lname, contect_no, email, password=None):
        user = self._create_user(
            fname = fname,
            lname = lname,
            contect_no = contect_no,
            email = email,
            password = password
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password = None):
        user = self._create_user(
            fname = 'Bhargav', 
            lname = 'Prajapati',
            contect_no = 9876543210,
            password = password,
            email = email
        )

        user.is_admin = True
        user.is_staff = True
        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    reg_no = models.AutoField(verbose_name = "Registration Number", primary_key = True, unique = True)

    fname = models.CharField(verbose_name = "First Name", max_length = 50)
    lname = models.CharField(verbose_name = "Last Name", max_length = 50)
    
    contect_no = models.IntegerField(verbose_name = "Contect No")
    email = models.EmailField(verbose_name = "Email ID", unique=True)
    
    # password = models.CharField(max_length = 20)
    
    clg_id = models.ForeignKey(Collages, verbose_name = "Collage", on_delete=models.SET_NULL, null=True, default = None)
    stream = models.ForeignKey(Stream, verbose_name = "Stream", on_delete=models.SET_NULL, null=True, default = None)

    is_participant = models.BooleanField(default=False, verbose_name = "Participant")
    is_admin = models.BooleanField(default=False, verbose_name = "Admin")
    is_staff = models.BooleanField(default = False, verbose_name = "Event Committee")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['reg_no', 'contect_no', 'email', 'fname', 'lname', 'clg_id', 'stream']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Event_Committee(models.Model):
    reg_no = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    committee_id = models.CharField(unique=True, max_length = 20)
    yearOfStudy = models.IntegerField()

    #Added as
    is_vol = models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)
    is_event_head = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    #want to work in
    in_sponsorship = models.BooleanField(default=False)
    in_publicity = models.BooleanField(default=False)
    in_criative =  models.BooleanField(default=False)
    in_technical = models.BooleanField(default=False)
    in_volunteering = models.BooleanField(default=False)
    in_logistics = models.BooleanField(default=False)
    in_graphics = models.BooleanField(default=False)
    in_eventManagement = models.BooleanField(default=False)

    
class Participant(models.Model):
    reg_no = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)

    def __str__(self):
        return User.objects.get(participant__reg_no = self.reg_no).email

class Volunteer(models.Model):
    reg_no = models.OneToOneField(Event_Committee, on_delete = models.CASCADE, primary_key = True)
    payment_hold = models.IntegerField(default = 0)
    isActive = models.BooleanField(default = False)

class Event_Head(models.Model):
    reg_no = models.OneToOneField(Event_Committee, on_delete = models.CASCADE, primary_key = True)
    isActive = models.BooleanField(default = False)

class Coordinator(models.Model):
    reg_no = models.OneToOneField(Event_Committee, on_delete = models.CASCADE, primary_key = True)
    payment_hold = models.IntegerField()
    isActive = models.BooleanField(default = False)

class Admin(models.Model):
    reg_no = models.OneToOneField(Event_Committee, on_delete = models.CASCADE, primary_key = True)
    isActive = models.BooleanField(default = False)
