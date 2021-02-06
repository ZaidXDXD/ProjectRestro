from django.urls import path

from home.views import home, tagpage, adddish

urlpatterns = [
    path("", home, name='home'),

    path("add_tag/",tagpage, name="addtag"),

    path('add_dish/', adddish, name="addDish"),
]
