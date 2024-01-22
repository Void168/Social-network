from django.forms import ModelForm

from .models import Page

class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = ('name', 'page_type', 'email', 'location', 'biography', 'business_hours_status', 'start_time', 'close_time', 'avatar', 'cover_image')

class PageProfileForm(ModelForm):
    class Meta:
        model = Page
        fields = ('email', 'name',)

class PageBiographyForm(ModelForm):
    class Meta:
        model = Page
        fields = ('biography',)

class PageTypeForm(ModelForm):
    class Meta:
        model = Page
        fields = ('page_type',)
        
class PageLocationForm(ModelForm):
    class Meta:
        model = Page
        fields = ('location',)