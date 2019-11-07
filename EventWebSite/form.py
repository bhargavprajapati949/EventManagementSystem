from django import forms
from django.contrib.auth.forms import UserCreationForm

from UserManager import User, Collages

class ParticipantRegForm(UserCreationForm):
    fname = forms.CharField(max_length=50)
    lname = forms.CharField(max_length=50)
    
    clg_id_choices = []
    for clg in Collages.objects.all():
        clg_id_choices += [clg.clg_id, clg.clg_name]

    clg_id = forms.ChoiceField(choices=clg_id_choices)

    email = forms.EmailField()
    contect_no = forms.IntegerField()

    password = forms.PasswordInput()
    confpassword = forms.PasswordInput()

    class Meta:
        model = User
        fields = ( 'fname', 'lname', 'clg_id', 'email', 'contect_no', 'password', 'confpassword', )

    def save(self, commit=True):
        user = super(ParticipantRegForm, self).save(commit=False)
        user.fname = self.cleaned_data['fname']
        user.lname = self.cleaned_data['lname']
        user.clg_id = self.cleaned_data['clg_id']
        user.email = self.cleaned_data['email']
        user.contect_no = self.cleaned_data['contect_no']
        user.password = self.cleaned_data['password']
        if commit:
            user.save()
        return user
        
        
