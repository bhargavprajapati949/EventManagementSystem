from django import forms
from django.contrib.auth.forms import UserCreationForm
from UserManager.models import Collages, User, Participant


class ParticipantRegForm(UserCreationForm):
    # fname = forms.CharField(max_length=50)
    # lname = forms.CharField(max_length=50)
    
    # clg_id_choices = (
    #     ('nu', 'nirma'),
    #     ('da', 'daiict'),
    # )
    # # for clg in Collages.objects.all():
    # #     clg_id_choices += [clg.clg_id, clg.clg_name]

    # clg_id = forms.ChoiceField(choices=clg_id_choices)

    # stream_choices = (
    #     ('Computer Eng', 'ce'), 
    #     ('Electrical Eng', 'ee'),
    #     ('Chemical Eng', 'ch'),
    #     ('Civil Eng', 'ci'),
    # )
    # stream = forms.ChoiceField(choices=stream_choices)

    # email = forms.EmailField()
    # contect_no = forms.IntegerField()

    # password = forms.PasswordInput()
    # confpassword = forms.PasswordInput()

    class Meta:
        model = User
        fields = ( 'fname', 'lname', 'clg_id', 'stream', 'email', 'contect_no' )

    def save(self):
        user = super(ParticipantRegForm, self).save(commit=False)
        user.fname = self.cleaned_data['fname']
        user.lname = self.cleaned_data['lname']
        user.email = self.cleaned_data['email']
        user.contect_no = self.cleaned_data['contect_no']
        user.clg_id = self.cleaned_data['clg_id']
        user.stream = self.cleaned_data['stream']
        user.is_participant = True

        Participant.objects.create(reg_no = user)
        # user.password = self.cleaned_data['password']
        
        user.save()
        return user
        
        
