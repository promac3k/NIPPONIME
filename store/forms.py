from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


# Crie seus formulários aqui.

class NewUserForm(UserCreationForm):
  email = forms.EmailField(required=True)
  
  
  class Meta:
    model = User
    fields = ("username",'first_name' ,'last_name',  "email", "password1", "password2")
  
  def save(self, commit=True):
    user = super(NewUserForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    
    if commit:
      user.save()
    
    return user

class ClientForm(forms.ModelForm):
  name = forms.CharField(required=True)  
  
  class Meta:
        model = Customer
        exclude = ("favorites", "user", "email")
  

class ContactForm(forms.Form):
  Name = forms.CharField(max_length = 50)
  Surname = forms.CharField(max_length = 50)
  Email = forms.EmailField(max_length = 150)
  Message = forms.CharField(widget = forms.Textarea, max_length = 2000)
  
