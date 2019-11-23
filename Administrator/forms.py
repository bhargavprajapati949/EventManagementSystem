from django import forms
from EventWebSite.models import news
from UserManager.models import Collages

class news_model_form(forms.ModelForm):    
    class Meta:
        model = news
        fields = ('for_whome', 'news_content', 'hyperlink')

class collage_model_form(forms.ModelForm):
    class Meta:
        model = Collages
        fields = ('clg_id','clg_name')
