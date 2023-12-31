from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'nickname','gender',)

class AvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)

class CoverImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('cover_image',)

class BiographyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('biography',)

class RelationshipForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('relationship_status','partner',)

class HomeTownForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('hometown',)

class LivingCityForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('living_city',)
