from django import forms
from django.forms.widgets import TextInput

from .models import Tag, Dishes

class TagForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': 'Add A Tag', 'autocomplete' : 'off', 'class': 'form-control'}))
    class Meta:
        model = Tag
        fields = "__all__"

class DishesForm(forms.ModelForm):
    description = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Dishes
        fields = ('name', 'price' ,'category', 'alcohol', 'food_tag' , "description", )

class DishesIconImageForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ('icon_image', )