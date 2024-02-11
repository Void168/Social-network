from django.forms import ModelForm

from .models import Group, Question, Rule

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

class GroupCoverImageForm(ModelForm):
    class Meta:
        model = Group
        fields = ('cover_image',)

class GroupRuleForm(ModelForm):
    class Meta:
        model = Rule
        fields = ('name','body',)