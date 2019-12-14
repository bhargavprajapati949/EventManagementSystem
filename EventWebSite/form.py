from django import forms
from django.contrib.auth.forms import UserCreationForm
from UserManager.models import User


class ParticipantRegForm(UserCreationForm):

    class Meta:
        model = User
        fields = ( 'fname', 'lname', 'clg', 'stream', 'email', 'contect_no' )

    def save(self):
        user = super(ParticipantRegForm, self).save(commit=False)
        user.fname = self.cleaned_data['fname']
        user.lname = self.cleaned_data['lname']
        user.email = self.cleaned_data['email']
        user.contect_no = self.cleaned_data['contect_no']
        user.clg = self.cleaned_data['clg']
        user.stream = self.cleaned_data['stream']
        user.is_participant = True

        user.save()

        return user
