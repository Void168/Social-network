from django.forms import ModelForm

from .models import Group

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name','is_private_group','show_group',)