from django import forms
from django.forms import ModelForm
from . models import * 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact 
        fields = ["full_name", "email", "subject", "message"]

    
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name","email", 
                  "password1", "password2"]
        
class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ["first_name", "last_name", "email", "phone", "profile_img"]