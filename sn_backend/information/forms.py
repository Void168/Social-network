from django import forms

from .models import Website, PhoneNumber, PageWebsite, PagePhoneNumber

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ('url','is_private','only_me',)
        
class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ('phone_number','is_private','only_me',)
        
class PageWebsiteForm(forms.ModelForm):
    class Meta:
        model = PageWebsite
        fields = ('url','is_private','only_me',)
        
class PagePhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PagePhoneNumber
        fields = ('phone_number','is_private','only_me',)