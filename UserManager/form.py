from django import forms
from django.contrib.auth.forms import UserCreationForm
from UserManager.models import Event_Commitee, User

class EventCommitteeRegForm(UserCreationForm):
    # fname = forms.CharField(max_length=50)
    # lname = forms.CharField(max_length=50)
    
    # contect_no = forms.IntegerField()
    # email = forms.CharField(max_length = 20)

    # password = forms.PasswordInput()
    # confpassword = forms.PasswordInput()

    # yearOfStudy = forms.IntegerField()
    # stream = forms.CharField(max_length = 100)

    class Meta:
        model = User
        fields = ( 'fname', 'lname', 'clg_id', 'stream', 'email', 'contect_no' )

    def save(self):
        user = super(EventCommitteeRegForm, self).save(commit=False)
        user.fname = self.cleaned_data['fname']
        user.lname = self.cleaned_data['lname']
        user.email = self.cleaned_data['email'] + "@nirmauni.ac.in"
        user.contect_no = self.cleaned_data['contect_no']
        user.clg_id = self.cleaned_data['clg_id']
        # user.password = self.cleaned_data['password']
        user.stream = self.cleaned_data['stream']
        user.is_event_commitee = True
        
        user.save()
        return user