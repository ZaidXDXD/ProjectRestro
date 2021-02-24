from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Models For Tags
class Tag(models.Model):
    COURSE_CATEGORY = (
        ('Beverage', 'Beverage'),
        ('Starter', 'Starter'),
        ('Main-Course', 'Main-Course'),
        ('Dessert', 'Dessert'),
    )
    name = models.CharField(max_length=255, null=True, unique=True)
    course = models.CharField(max_length=65, null=True, choices=COURSE_CATEGORY)
    def __str__(self):
        return self.name

# For Icon Image
def get_icon_image_file_path(self, filename):
    return f"DishImages/{str(self.pk)}/icon_image.png"

def get_default_icon_image():
    return 'Restro/default_icon_image.jpg'


# For Major Image
def get_major_image_file_path(self, filename):
    return f"DishImages/{str(self.pk)}/major_image.png"

def get_default_major_iamge():
    return 'Restro/default_major_image.jpg'

# For Secondary Image
def get_secondary_image_file_path(self, filename):
    return f"DishImages/{str(self.pk)}/secondary_image.png"

def get_default_secondary_iamge():
    return 'Restro/default_secondary_image.jpg'

# For Tertiary Image
def get_tertiary_image_file_path(self, filename):
    return f"DishImages/{str(self.pk)}/tertiary_image.png"

def get_default_tertiary_iamge():
    return 'Restro/default_tertiary_image.jpg'

# Model For Dishes (Need to add star rating and Image Description)
class Dishes(models.Model):
    CATEGORY_CHOICES = (
        ('Veg', "Veg")
        ,("Non-Veg", "Non-Veg")
    )
    ALCOHOL_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    name = models.CharField(max_length=255, null=True, unique=True)
    date_created = models.DateTimeField(null=True, auto_now_add=True)
    description = models.TextField(blank=True) 
    price = models.FloatField(null=True)
    food_tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, null=True)
    category = models.CharField(max_length=10, null=True, choices=CATEGORY_CHOICES)
    alcohol = models.CharField(max_length=10, null=True, choices=ALCOHOL_CHOICES)
    icon_image = models.ImageField(null=True,blank=True, upload_to=get_icon_image_file_path, default=get_default_icon_image)
    major_image = models.ImageField(null=True,blank=True, upload_to=get_major_image_file_path, default=get_default_major_iamge)
    major_description = models.CharField(max_length=40, blank=True)
    secondary_image = models.ImageField(null=True,blank=True, upload_to=get_secondary_image_file_path, default=get_default_secondary_iamge)
    secondary_description = models.CharField(max_length=40, blank=True)
    tertiary_image = models.ImageField(null=True,blank=True,  upload_to=get_tertiary_image_file_path, default=get_default_tertiary_iamge)
    tertiary_description = models.CharField(max_length=40, blank=True)
    dish_view = models.IntegerField(default=0, null=True,blank=True)
    
    def __str__(self):
        return self.name


#Model For Cart
class Cart(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Canelled', 'Canelled'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    quantity = models.IntegerField(null=True)
    total_amount = models.FloatField(null=True)
    table_number = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.customer.username} Ordered {self.ordered_dish.name}"
