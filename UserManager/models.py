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
    def create_user(self, email, username, password=None):
    
        user=self.model(
            email=self.normalize_email(email), 
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        # user = self.create_superuser(
        #     email = self.normalize_email(email), 
        #     password = password,
        #     username = username,
        # )
        # user.is_superuser = True

        user = self.model(username = username)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    reg_no = models.AutoField(primary_key = True)

    fname = models.CharField(max_length = 50)
    lname = models.CharField(max_length = 50)
    
    contect_no = models.IntegerField()
    email = models.EmailField(unique=True)
    
    # password = models.CharField(max_length = 20)
    
    clg_id = models.ForeignKey(Collages, on_delete=models.SET_DEFAULT, default = 0)
    stream = models.ForeignKey(Stream, on_delete=models.SET_DEFAULT, default = 0)

    is_participant = models.BooleanField(default=False)
    is_event_commitee = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['reg_no', 'contect_no', 'email', 'fname', 'lname', 'clg_id', 'stream']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Event_Commitee(models.Model):
    reg_no = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    commitee_id = models.CharField(unique=True, max_length = 20)
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

class Publicity_Volunteer(models.Model):
    reg_no = models.OneToOneField(Event_Commitee, on_delete = models.CASCADE, primary_key = True)
    payment_hold = models.IntegerField()
    isActive = models.BooleanField(default = False)

class Event_Head(models.Model):
    reg_no = models.OneToOneField(Event_Commitee, on_delete = models.CASCADE, primary_key = True)
    isActive = models.BooleanField(default = False)

class Coordinator(models.Model):
    reg_no = models.OneToOneField(Event_Commitee, on_delete = models.CASCADE, primary_key = True)
    payment_hold = models.IntegerField()
    isActive = models.BooleanField(default = False)

class Admin(models.Model):
    reg_no = models.OneToOneField(Event_Commitee, on_delete = models.CASCADE, primary_key = True)
    isActive = models.BooleanField(default = False)
