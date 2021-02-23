from django import forms
from django.forms.widgets import TextInput

from .models import (
    Tag, 
    Dishes, 
    Cart,
)

# Form -> Add Tag 
class TagForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=TextInput(attrs={'placeholder': 'Add A Tag', 'autocomplete' : 'off', 'class': 'form-control' }))
    class Meta:
        model = Tag
        fields = "__all__"        


# Form -> Add Dish Details
class DishesForm(forms.ModelForm):
    description = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Dishes
        fields = ('name', 'price' ,'category', 'alcohol', 'food_tag' , "description", )

# Form -> Dish Icon Image
class DishesIconImageForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ('icon_image', )
    
# Form -> Dish Major Image    
class DishesMajorImageForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ('major_image', 'major_description', )

# Form -> Dish Secondary Image
class DishesSecondaryImageForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ('secondary_image', 'secondary_description',)
    
# Form -> Dish Tertiary Image
class DishesTertiaryImageForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ('tertiary_image', 'tertiary_description',)


# Form -> Dish Edit Form.
class EditDishForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = (
                    'name', 
                    'price',
                    'category', 
                    'alcohol', 
                    'food_tag', 
                    "description",
                    'icon_image',
                    'major_image', 
                    'major_description',
                    'secondary_image', 
                    'secondary_description',
                    'tertiary_image', 
                    'tertiary_description',
                 )

# Form -> Cart Form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('customer','ordered_dish', 'quantity', 'total_amount', "table_number")