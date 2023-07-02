'''
Shortener Forms urlshortener/forms.py
'''

from django import forms

from .models import Shortener

class ShortenerForm(forms.ModelForm):
    
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control form-control-md", "placeholder": "https://example.com/my-long-url","style":"color:#96b4e0;",}))
    
    class Meta:
        model = Shortener

        fields = ('long_url',)
