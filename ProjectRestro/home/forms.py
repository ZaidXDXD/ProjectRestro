from django import forms
from django.forms.widgets import TextInput

from .models import (
    Tag, 
    Dishes, 
    Order,
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
        fields = ('major_image', )

# Form -> Dish Secondary Image
class DishesSecondaryImageForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ('secondary_image', )
    
# Form -> Dish Tertiary Image
class DishesTertiaryImageForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ('tertiary_image', )


# Form -> Dish Edit Form.
class EditDishForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = "__all__"

# Form -> Order Form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer','ordered_dish', 'quantity', 'total_amount', "table_number")