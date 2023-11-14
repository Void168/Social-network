from django import forms

from .models import Website, PhoneNumber

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ('url',)
        
class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ('phone_number',)