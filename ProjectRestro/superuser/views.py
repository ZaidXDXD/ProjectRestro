from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from home.models import (
    Cart, 
    Dishes, 
    Tag
)

from .decorators import allowed_users

# Create your views here.

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def adminDish(request,*args, **kwargs):
    dishes = Dishes.objects.all()
    tags = Tag.objects.all()
    beverages = {}
    starters = {}
    main_course = {}
    desserts = {}
    tags = Tag.objects.all()

    for tag in tags:
        if tag.course == 'Beverage':
            beverages[tag.name] = tag.name
        elif tag.course == 'Starter':
            starters[tag.name] = tag.name
        elif tag.course == 'Main-Course':
            main_course[tag.name] = tag.name
        else:
            desserts[tag.name] = tag.name

    beverage_dishes = []
    starter_dishes = []
    main_course_dishes = []
    dessert_dishes = []

    for dish in dishes:
        if dish.food_tag.name in beverages:
            beverage_dishes.append(dish)
        elif dish.food_tag.name in starters:
            starter_dishes.append(dish)
        elif dish.food_tag.name in main_course:
            main_course_dishes.append(dish)
        else:
            dessert_dishes.append(dish)
    context  = {
                    "beverages" : beverages,
                    "starters" : starters, 
                    "main_course" : main_course, 
                    "desserts" : desserts, 
                    'beverage_dishes' : beverage_dishes, 
                    'starter_dishes' : starter_dishes, 
                    'main_course_dishes' : main_course_dishes,
                    'dessert_dishes' : dessert_dishes
                }
    return render(request, 'superuser/AdminDishPage.html', context)

