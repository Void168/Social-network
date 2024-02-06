from django.forms import ModelForm

from .models import Group, Question

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name','is_private_group','show_group',)
        
class GroupInfoForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name','biography',)
        
class GroupWebsiteForm(ModelForm):
    class Meta:
        model = Group
        fields = ('website',)
        
class GroupQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('body',)