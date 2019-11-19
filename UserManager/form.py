from django import forms
from django.contrib.auth.forms import UserCreationForm
from UserManager.models import Event_Commitee

class EventCommitteeRegForm(UserCreationForm):
    fname = forms.CharField(max_length=50)
    lname = forms.CharField(max_length=50)
    
    email = forms.CharField(max_length = 20)
    contect_no = forms.IntegerField()

    password = forms.PasswordInput()
    confpassword = forms.PasswordInput()

    year = forms.IntegerField()
    stream = forms.CharField(max_length = 100)

    class Meta:
        model = User
        fields = ( 'fname', 'lname', 'clg_id', 'stream', 'email', 'contect_no', 'password', 'confpassword', )

    def save(self, commit=True):
        user = super(EventCommitteeRegForm, self).save(commit=False)
        user.fname = self.cleaned_data['fname']
        user.lname = self.cleaned_data['lname']
        user.clg_id = self.cleaned_data['clg_id']
        user.email = self.cleaned_data['email'] + "@nirmauni.ac.in"
        user.contect_no = self.cleaned_data['contect_no']
        user.password = self.cleaned_data['password']
        user.year = self.cleaned_data['year']
        user.stream = self.cleaned_data['stream']

        

        if commit:
            user.save()
        return user
