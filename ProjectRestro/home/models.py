from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


<<<<<<< HEAD
=======
# Models For Tags
>>>>>>> a17b769d86840eb651aba493fc91b34799d54cc5
class Tag(models.Model):
    name = models.CharField(max_length=255, null=True, unique=True)
    def __str__(self):
        return self.name

<<<<<<< HEAD
=======

# For Icon Image
>>>>>>> a17b769d86840eb651aba493fc91b34799d54cc5
def get_icon_image_file_path(self, filename):
    return f"DishImages/{str(self.pk)}/icon_image.png"

def get_default_icon_image():
    return 'Restro/default_icon_image.jpg'


<<<<<<< HEAD
=======
# For Major Image
>>>>>>> a17b769d86840eb651aba493fc91b34799d54cc5
def get_major_image_file_path(self, filename):
    return f"DishImages/{str(self.pk)}/major_image.png"

def get_default_major_iamge():
    return 'Restro/default_major_image.jpg'

<<<<<<< HEAD
=======

# For Secondary Image
>>>>>>> a17b769d86840eb651aba493fc91b34799d54cc5
def get_secondary_image_file_path(self, filename):
    return f"DishImages/{str(self.pk)}/secondary_image.png"

def get_default_secondary_iamge():
    return 'Restro/default_secondary_image.jpg'

<<<<<<< HEAD
=======

# For Tertiary Image
>>>>>>> a17b769d86840eb651aba493fc91b34799d54cc5
def get_tertiary_image_file_path(self, filename):
    return f"DishImages/{str(self.pk)}/tertiary_image.png"

def get_default_tertiary_iamge():
    return 'Restro/default_tertiary_image.jpg'

<<<<<<< HEAD
=======

# Model For Dishes
>>>>>>> a17b769d86840eb651aba493fc91b34799d54cc5
class Dishes(models.Model):
    CATEGORY_CHOICES = (
        ('Veg', "Veg")
        ,("Non-Veg", "Non-Veg")
    )
    ALCOHOL_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    name = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(null=True, auto_now_add=True)
    description = models.TextField(blank=True) 
    price = models.FloatField(null=True)
    food_tag = models.ManyToManyField(Tag)
    category = models.CharField(max_length=10, null=True, choices=CATEGORY_CHOICES)
    alcohol = models.CharField(max_length=10, null=True, choices=ALCOHOL_CHOICES)
    like = models.ManyToManyField(User, blank=True) 
    icon_image = models.ImageField(null=True,blank=True, upload_to=get_icon_image_file_path, default=get_default_icon_image)
    major_image = models.ImageField(null=True,blank=True, upload_to=get_major_image_file_path, default=get_default_major_iamge)
    secondary_image = models.ImageField(null=True,blank=True, upload_to=get_secondary_image_file_path, default=get_default_secondary_iamge)
    tertiary_image = models.ImageField(null=True,blank=True,  upload_to=get_tertiary_image_file_path, default=get_default_tertiary_iamge)

    def __str__(self):
<<<<<<< HEAD
        return self.name
=======
        return self.name
>>>>>>> a17b769d86840eb651aba493fc91b34799d54cc5
