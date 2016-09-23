from .models import News
from django import forms

class newsForm(forms.ModelForm):
    class Meta:
         model = News
         fields = ('category',)
         widgets = {
            'category': forms.TextInput(attrs={'id':'news_categories',})
    	}

