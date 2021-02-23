from django.urls import path
from superuser.views import adminDish

urlpatterns = [
    path('dish/', adminDish, name="adminDishPage")
]