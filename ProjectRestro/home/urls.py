from django.urls import path

from home.views import home, tagpage

urlpatterns = [
    path("", home, name='home'),

    path("add_tag/",tagpage, name="addtag"),
]