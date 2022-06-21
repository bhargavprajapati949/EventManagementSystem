from dataclasses import field
from django import forms

from EventWebSite.models import news, Event, Participants
from EventHead.models import Event_Head
from Coordinator.models import Coordinator
from UserManager.models import College, Stream, User

class registers_model_form(forms.ModelForm):
    class Meta:
        model = Participants
        fields = ('remark',)

class participant_user_model_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('fname', 'lname', 'contect_no', 'email', 'clg', 'stream')

class event_model_form(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_id', 'event_name', 'event_detail', 'rules', 'event_logo', 'event_status', 'venue', 'date_time', 'fees')
        help_texts = {
            'date_time' : 'MM/DD/YYYY HH:MM format'
        }

class news_model_form(forms.ModelForm):    
    class Meta:
        model = news
        fields = ('news_content', 'hyperlink')
    
    def __init__(self, *args, **kwargs):
        super(news_model_form, self).__init__(*args, **kwargs)
        self.fields['hyperlink'].required = False

class collage_model_form(forms.ModelForm):
    class Meta:
        model = College
        fields = ('clg_id','clg_name')

class stream_model_form(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ('stream_id', 'stream_name')

class event_head_model_form(forms.ModelForm):
    class Meta:
        model = Event_Head
        fields = ('reg_no', 'event')

    def save(self):
        event_head = super(event_head_model_form, self).save(commit=False)
        event_head.isActive = True
        event_head.save()
        return event_head

class event_head_isActive_form(forms.ModelForm):
    class Meta:
        model = Event_Head
        fields = ('isActive',)

class coordinator_model_form(forms.ModelForm):

    class Meta:
        model = Coordinator
        fields = ('reg_no',)

    def save(self):
        coordinator = super(coordinator_model_form, self).save(commit=False)
        coordinator.isActive = True
        coordinator.save()
        return coordinator

class coordinator_isActive_form(forms.ModelForm):
    class Meta:
        model = Coordinator
        fields = ('isActive',)