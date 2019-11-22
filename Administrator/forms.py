from django import forms
from EventWebSite.models import news

class news_model_form(forms.ModelForm):    
    class Meta:
        model = news
        fields = ('for_whome', 'news_content', 'hyperlink')

    # def is_valid(self):
    #     valid = super(news_model_form, self).is_valid()
    #     print(valid)
    #     return True
