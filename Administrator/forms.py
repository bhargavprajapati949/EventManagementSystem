from django import forms
from EventWebSite.models import news

class addnews_form(forms.ModelForm):    
    class Meta:
        model = news
        fields = ('for_whome', 'news_content', 'hyperlink')

