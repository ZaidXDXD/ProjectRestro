from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

from .models import Profile


class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': 'Username', 'autocomplete' : 'off'}))
    email = forms.CharField(max_length=255,required=True,widget=forms.EmailInput(attrs={'placeholder' : 'Email', 'autocomplete' : 'off'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        """
        ensure that email is always lower case.
        """
        return self.cleaned_data['email'].lower()


class ProfileForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'max' : date.today()}))
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'name', 'email']
