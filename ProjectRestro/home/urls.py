from django.urls import path

from home.views import (
    home,
    tagpage,
    adddish,
    crop_icon_image,
    add_dish_image_icon, 
     
)

urlpatterns = [
    path("", home, name='home'),

    path("add_tag/",tagpage, name="addtag"),

    path('add_dish/', adddish, name="addDish"),

    path('add_dish/addIconImage/<dish_id>',add_dish_image_icon , name="addIconImage"),
    path('add_dish/addIconImage/<dish_id>/cropIconImage/',crop_icon_image, name="crop_icon_image" ),
]
