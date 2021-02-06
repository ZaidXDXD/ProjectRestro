from django import forms
from django.forms.widgets import TextInput

from .models import Tag

class TagForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': 'Add A Tag', 'autocomplete' : 'off', 'class': 'form-control'}))
    class Meta:
        model = Tag
        fields = "__all__"