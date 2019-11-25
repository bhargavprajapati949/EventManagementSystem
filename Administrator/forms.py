from django import forms
from EventWebSite.models import news, Event
from UserManager.models import Collages, Stream, Volunteer

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
        fields = ('for_whome', 'news_content', 'hyperlink')

class collage_model_form(forms.ModelForm):
    class Meta:
        model = Collages
        fields = ('clg_id','clg_name')

class stream_model_form(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ('stream_id', 'stream_name')

class volunteer_model_form(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('reg_no',)
