from django.forms import ModelForm

from .models import Page

class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = ('name', 'page_type', 'email', 'location', 'biography', 'business_hours_status', 'start_time', 'close_time', 'avatar', 'cover_image')
    