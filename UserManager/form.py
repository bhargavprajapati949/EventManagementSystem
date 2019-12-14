from django import forms
from django.contrib.auth.forms import UserCreationForm
from UserManager.models import  User, Event_Committee

class EventCommitteeRegForm(UserCreationForm):
    # fname = forms.CharField(max_length=50)
    # lname = forms.CharField(max_length=50)
    
    # contect_no = forms.IntegerField()
    # email = forms.CharField(max_length = 20)

    # password = forms.PasswordInput()
    # confpassword = forms.PasswordInput()

    # yearOfStudy = forms.IntegerField()
    # rollno = forms.CharField(max_length = 10)
    # stream = forms.CharField(max_length = 100)


    class Meta:
        model = User
        fields = ( 'fname', 'lname', 'clg', 'stream', 'email', 'contect_no' )

    def save(self):
        user = super(EventCommitteeRegForm, self).save(commit=False)
        user.fname = self.cleaned_data['fname']
        user.lname = self.cleaned_data['lname']
        user.email = self.cleaned_data['email']
        user.contect_no = self.cleaned_data['contect_no']
        user.clg = self.cleaned_data['clg']
        # user.password = self.cleaned_data['password']
        user.stream = self.cleaned_data['stream']
        user.is_event_commitee = True
        user.save()

        # Event_Commitee.objects.create()
        # member = Event_Commitee(reg_no = user)
        # member.commitee_id = self.cleaned_data['rollno']
        # member.yearOfStudy = self.cleaned_data['yearOfStudy']
        # member.save()
        return user

class EventCommitteeDetailForm(forms.ModelForm):
    class Meta:
        model = Event_Committee
        fields = ('committee_id', 'yearOfStudy', 'in_sponsorship', 'in_publicity', 'in_criative', 'in_technical', 'in_volunteering', 'in_logistics', 'in_graphics', 'in_eventManagement')
        