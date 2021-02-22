import base64
import json
import os

import cv2
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import files
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .decorators import allowed_users
from .forms import (
    TagForm,
    DishesForm, 
    DishesIconImageForm, 
    DishesMajorImageForm,
    DishesSecondaryImageForm,
    DishesTertiaryImageForm,
    EditDishForm,
    OrderForm,
)
from .models import (
    Tag, 
    Dishes,
    Cart
)
from requests.api import request

def home(request):
    return render(request, 'home/home.html')


# View For Tags
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def tagpage(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            redirect ('addtag')
    else:
        form = TagForm()
    return render(request, 'home/tag.html', {'form':form})

# View For Add Dish
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def adddish(request):
    tags = Tag.objects.all().order_by('name')
    if request.method == "POST":
        form = DishesForm(request.POST)
        if form.is_valid():
            dish = form.save()
            return redirect('addIconImage', dish.pk )
    else:
        form = DishesForm()
    return render(request, 'home/Add_New_Dish_Details.html', {'tags' : tags, "form" : form})

# View for showing the menu page
def menuPage(request):
    cnt = range(100)

    dishes = Dishes.objects.all()

    # ----------------------------------------
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

    dishes = Dishes.objects.all()

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
    # ----------------------------------------

    context = {"cnt" : cnt, "beverages" : beverages, "starters" : starters, "main_course" : main_course, "desserts" : desserts, 'beverage_dishes' : beverage_dishes, 'starter_dishes' : starter_dishes, 'main_course_dishes' : main_course_dishes, 'dessert_dishes' : dessert_dishes}
    return render(request, 'home/menu.html', context)

# View For Add Icon Image

# Address Where All The Temp Icon Image Are Stored 
TEMP_ICON_IMAGE_NAME = "temp_icon_image.png"

# Function To Get The Location Where Temp Icon Image Is Store 
def save_temp_icon_image_from_base64String(imageString, dish):
    INCORRECT_PADDING_EXCEPTION = "Incorrect Padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + "/" + str(dish.pk)):
            os.mkdir(settings.TEMP + "/" + str(dish.pk))
        url = os.path.join(settings.TEMP + "/" + str(dish.pk), TEMP_ICON_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        print('Exception: ' + str(e))
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += '=' * ((4 - len(imageString) % 4) % 4)
            return save_temp_icon_image_from_base64String(imageString, dish)
    return None


# Function To Get The Cropped Icon Image
def crop_icon_image(request, *args, **kwargs):
    payload = {}
    dish_id = kwargs.get('dish_id')
    dish = Dishes.objects.get(pk=dish_id)
    if request.POST:
        try: 
            imageString = request.POST.get("icon_image")
            url = save_temp_icon_image_from_base64String(imageString, dish)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get('cropX_icon'))))
            cropY = int(float(str(request.POST.get('cropY_icon'))))
            cropWidth = int(float(str(request.POST.get('cropWidth_icon'))))
            cropHeight = int(float(str(request.POST.get('cropHeight_icon'))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

            crop_img = cv2.resize(crop_img,(400,400))
            cv2.imwrite(url, crop_img)

            if(os.path.normpath(dish.icon_image.url) != "\media\Restro\default_icon_image.jpg"):
                dish.icon_image.delete()

            dish.icon_image.save('icon_image.png', files.File(open(url, "rb")))

            dish.save()

            payload['result'] = "success"
            payload['cropped_icon_image'] = dish.icon_image.url 

            os.remove(url)
            
        except Exception as e:
            print("Exception: " + str(e))
            payload['result'] = 'error'
            payload['exception'] = str(e)
    
    return HttpResponse(json.dumps(payload), content_type="application/json")

# Main View Function From To Add Icon Image
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def add_dish_image_icon(request, *args, **kwargs):
    dish_id = kwargs.get('dish_id')
    dish_profile = Dishes.objects.get(pk=dish_id)
    context = {}
    context['dish'] = dish_profile
    if request.POST:
        form = DishesIconImageForm(request.POST, request.FILES, instance=dish_profile)
        if form.is_valid():
            image_url = form.cleaned_data['icon_image']
            if(image_url == "Restro/default_icon_image.jpg"):
                messages.info(request, "No Image Uploades!")
                return redirect('addIconImage',dish_profile.pk)
            else:
                form.save()
                return redirect('addMajorImage', dish_profile.pk)
        else:
            form = DishesIconImageForm(request.POST, instance=dish_profile,
                initial={
                    "id" : dish_profile.id,
                    'icon_image': dish_profile.icon_image,
                })
            context['form'] = form

    else:
        form = DishesIconImageForm(
            initial={
                    "id" : dish_profile.id,
                    'icon_image': dish_profile.icon_image,
                }
        )
        context['form'] = form
    
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'home/Add_New_Dish_Icon_Image.html', context)


# View For Add Major Image

# Address Where All The Temp Major Image Are Stored 
TEMP_MAJOR_IMAGE_NAME = "temp_major_image.png"


# Function To Get The Location Where Temp Major Image Is Store 
def save_temp_major_image_from_base64String(imageString, dish):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + "/" + str(dish.pk)):
            os.mkdir(settings.TEMP + "/" + str(dish.pk))
        url = os.path.join(settings.TEMP + "/" + str(dish.pk), TEMP_MAJOR_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        print('exception: ' + str(e))
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += '=' * ((4 - len(imageString) % 4) % 4)
            return save_temp_major_image_from_base64String(imageString, dish)
    return None

# Function To Get The Cropped Major Image
def crop_major_image(request, *args, **kwargs):
    payload = {}
    dish_id = kwargs.get('dish_id')
    dish = Dishes.objects.get(pk=dish_id)
    if request.POST:
        try: 
            imageString = request.POST.get("major_image")
            url = save_temp_major_image_from_base64String(imageString, dish)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get('cropX_major'))))
            cropY = int(float(str(request.POST.get('cropY_major'))))
            cropWidth = int(float(str(request.POST.get('cropWidth_major'))))
            cropHeight = int(float(str(request.POST.get('cropHeight_major'))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]
            
            crop_img = cv2.resize(crop_img,(900,900))
            cv2.imwrite(url, crop_img)

            if(os.path.normpath(dish.major_image.url) != "\media\Restro\default_major_image.jpg"):
                dish.major_image.delete()

            dish.major_image.save('major_image.png', files.File(open(url, "rb")))

            dish.save()

            payload['result'] = "success"
            payload['cropped_major_image'] = dish.major_image.url 

            os.remove(url)
            
        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = 'error'
            payload['exception'] = str(e)
    
    return HttpResponse(json.dumps(payload), content_type ="application/json")


# Main View Function To Add Major Image
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def add_dish_image_major(request, *args, **kwargs):
    dish_id = kwargs.get('dish_id')
    dish_profile = Dishes.objects.get(pk=dish_id)
    context = {}
    context['dish'] = dish_profile
    if request.POST:
        form = DishesMajorImageForm(request.POST, request.FILES, instance=dish_profile)
        if form.is_valid():
            image_url = form.cleaned_data['major_image']
            if(image_url == "Restro/default_major_image.jpg"):
                messages.info(request, "No Image Uploades!")
                return redirect('addMajorImage',dish_profile.pk)
            else:
                form.save()
                return redirect('addSecondaryImage', dish_profile.pk)
        else:
            form = DishesMajorImageForm(request.POST, instance=dish_profile,
                initial={
                    "id" : dish_profile.id,
                    'major_image': dish_profile.major_image,
                    'major_description': dish_profile.major_description,
                })
            context['form'] = form

    else:
        form = DishesMajorImageForm(
            initial={
                    "id" : dish_profile.id,
                    'major_image': dish_profile.major_image,
                    'major_description': dish_profile.major_description,
                }
        )
        context['form'] = form
    
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'home/Add_New_Dish_Major_Image.html', context)


# View For Add Secondary Image

# Address Where All The Temp Secondary Image Are Stored 
TEMP_SECONDARY_IMAGE_NAME = "temp_secondary_image.png"

# Function To Get The Path For Where Temp Secondary Images Are Stored
def save_temp_secondary_image_from_base64String(imageString, dish):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + "/" + str(dish.pk)):
            os.mkdir(settings.TEMP + "/" + str(dish.pk))
        url = os.path.join(settings.TEMP + "/" + str(dish.pk), TEMP_SECONDARY_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        print('exception: ' + str(e))
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += '=' * ((4 - len(imageString) % 4) % 4)
            return save_temp_secondary_image_from_base64String(imageString, dish)
    return None


# Function To Get Cropped Secondary Image
def crop_secondary_image(request, *args, **kwargs):
    payload = {}
    dish_id = kwargs.get('dish_id')
    dish = Dishes.objects.get(pk=dish_id)
    if request.POST:
        try: 
            imageString = request.POST.get("secondary_image")
            url = save_temp_secondary_image_from_base64String(imageString, dish)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get('cropX_secondary'))))
            cropY = int(float(str(request.POST.get('cropY_secondary'))))
            cropWidth = int(float(str(request.POST.get('cropWidth_secondary'))))
            cropHeight = int(float(str(request.POST.get('cropHeight_secondary'))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

            crop_img = cv2.resize(crop_img,(900,900))
            cv2.imwrite(url, crop_img)

            if(os.path.normpath(dish.secondary_image.url) != "\media\Restro\default_secondary_image.jpg"):
                dish.secondary_image.delete()

            dish.secondary_image.save('secondary_image.png', files.File(open(url, "rb")))

            dish.save()

            payload['result'] = "success"
            payload['cropped_secondary_image'] = dish.secondary_image.url 

            os.remove(url)
            
        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = 'error'
            payload['exception'] = str(e)
    
    return HttpResponse(json.dumps(payload), content_type ="application/json")


# Main Function For Secondary Image
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def add_dish_image_secondary(request, *args, **kwargs):
    dish_id = kwargs.get('dish_id')
    dish_profile = Dishes.objects.get(pk=dish_id)
    context = {}
    context['dish'] = dish_profile
    if request.POST:
        form = DishesSecondaryImageForm(request.POST, request.FILES, instance=dish_profile)
        if form.is_valid():
            image_url = form.cleaned_data['secondary_image']
            if(image_url == "Restro/default_secondary_image.jpg"):
                messages.info(request, "No Image Uploades!")
                return redirect('addSecondaryImage',dish_profile.pk)
            else:
                form.save()
                return redirect('addTertiaryImage', dish_profile.pk)
        else:
            form = DishesSecondaryImageForm(request.POST, instance=dish_profile,
                initial={
                    "id" : dish_profile.id,
                    'secondary_image': dish_profile.secondary_image,
                    'secondary_description': dish_profile.secondary_description,
                })
            context['form'] = form

    else:
        form = DishesSecondaryImageForm(
            initial={
                    "id" : dish_profile.id,
                    'secondary_image': dish_profile.secondary_image,
                    'secondary_description': dish_profile.secondary_description,
                }
        )
        context['form'] = form
    
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'home/Add_New_Dish_Secondary_Image.html', context)




# View For Add Tertiary Image

# Address Where All The Temp Tertiary Image Are Stored
TEMP_TERTIARY_IMAGE_NAME = "temp_tertiary_image.png"

# Function To Get The Path For Where Temp Tertiary Images Are Stored
def save_temp_tertiary_image_from_base64String(imageString, dish):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + "/" + str(dish.pk)):
            os.mkdir(settings.TEMP + "/" + str(dish.pk))
        url = os.path.join(settings.TEMP + "/" + str(dish.pk), TEMP_TERTIARY_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        print('exception: ' + str(e))
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += '=' * ((4 - len(imageString) % 4) % 4)
            return save_temp_tertiary_image_from_base64String(imageString, dish)
    return None


# Function To Get Cropped Tertiary Image
def crop_tertiary_image(request, *args, **kwargs):
    payload = {}
    dish_id = kwargs.get('dish_id')
    dish = Dishes.objects.get(pk=dish_id)
    if request.POST:
        try: 
            imageString = request.POST.get("tertiary_image")
            url = save_temp_tertiary_image_from_base64String(imageString, dish)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get('cropX_tertiary'))))
            cropY = int(float(str(request.POST.get('cropY_tertiary'))))
            cropWidth = int(float(str(request.POST.get('cropWidth_tertiary'))))
            cropHeight = int(float(str(request.POST.get('cropHeight_tertiary'))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

            crop_img = cv2.resize(crop_img,(900,900))
            cv2.imwrite(url, crop_img)

            if(os.path.normpath(dish.tertiary_image.url) != "\media\Restro\default_tertiary_image.jpg"):
                dish.tertiary_image.delete()

            dish.tertiary_image.save('tertiary_image.png', files.File(open(url, "rb")))

            dish.save()

            payload['result'] = "success"
            payload['cropped_tertiary_image'] = dish.tertiary_image.url 

            os.remove(url)
            
        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = 'error'
            payload['exception'] = str(e)
    
    return HttpResponse(json.dumps(payload), content_type ="application/json")


# Main Function For Tertiary Image
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def add_dish_image_tertiary(request, *args, **kwargs):
    dish_id = kwargs.get('dish_id')
    dish_profile = Dishes.objects.get(pk=dish_id)
    context = {}
    context['dish'] = dish_profile
    if request.POST:
        form = DishesTertiaryImageForm(request.POST, request.FILES, instance=dish_profile)
        if form.is_valid():
            image_url = form.cleaned_data['tertiary_image']
            if(image_url == "Restro/default_tertiary_image.jpg"):
                messages.info(request, "No Image Uploades!")
                return redirect('addTertiaryImage',dish_profile.pk)
            else:
                form.save()
                return redirect('editDish', dish_profile.pk)
        else:
            form = DishesTertiaryImageForm(request.POST, instance=dish_profile,
                initial={
                    "id" : dish_profile.id,
                    'tertiary_image': dish_profile.tertiary_image,
                    'tertiary_description': dish_profile.tertiary_description, 
                })
            context['form'] = form

    else:
        form = DishesTertiaryImageForm(
            initial={
                    "id" : dish_profile.id,
                    'tertiary_image': dish_profile.tertiary_image,
                    'tertiary_description': dish_profile.tertiary_description, 
                }
        )
        context['form'] = form
    
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'home/Add_New_Dish_Tertiary_Image.html', context)


# Function To Edit Dish
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def edit_dish(request, *args, **kwargs):
    tags = Tag.objects.all().order_by('name')
    dish_id = kwargs.get('dish_id')
    dish = Dishes.objects.get(pk=dish_id)
    context = {}
    context['tags'] = tags
    context['dish_name'] = dish.name
    if request.POST:
        form = EditDishForm(request.POST, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('home')
            
        else:
            form = EditDishForm(request.POST, instance=dish,
                initial={
                    'id': dish.id,
                    'name': dish.name,
                    'tag' : dish.food_tag,
                    'price': dish.price,
                    'category': dish.category,
                    'alcohol' : dish.alcohol,
                    'description': dish.description,
                    'icon_image' : dish.icon_image,
                    'major_image': dish.major_image,
                    'secondary_image': dish.secondary_image,
                    'tertiary_image': dish.tertiary_image,
                    'major_description': dish.major_description,
                    'secondary_description': dish.secondary_description,
                    'tertiary_description': dish.tertiary_description,                      
                }
            )
    else:
        form = EditDishForm(
                initial={
                    'id': dish.id,
                    'name': dish.name,
                    'tag' : dish.food_tag,
                    'price': dish.price,
                    'category': dish.category,
                    'alcohol' : dish.alcohol,
                    'description': dish.description,
                    'icon_image' : dish.icon_image,
                    'major_image': dish.major_image,
                    'secondary_image': dish.secondary_image,
                    'tertiary_image': dish.tertiary_image, 
                    'major_description': dish.major_description,
                    'secondary_description': dish.secondary_description,
                    'tertiary_description': dish.tertiary_description,                     
                }
            ) 

    context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'home/Edit_Dish.html', context)


# Function To Delete A Dish
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def delete_dish(request, *args, **kwargs):
    dish_id = kwargs.get('dish_id')
    dish = Dishes.objects.get(pk=dish_id)

    if(os.path.normpath(dish.icon_image.url) != "\media\Restro\default_icon_image.jpg"):
        dish.icon_image.delete()

    if(os.path.normpath(dish.major_image.url) != "\media\Restro\default_major_image.jpg"):
        dish.major_image.delete()

    if(os.path.normpath(dish.secondary_image.url) != "\media\Restro\default_secondary_image.jpg"):
        dish.secondary_image.delete()

    if(os.path.normpath(dish.tertiary_image.url) != "\media\Restro\default_tertiary_image.jpg"):
        dish.tertiary_image.delete()

    dish.delete()

    return redirect('home')


#Function To Get Table Number
def returnTableNumber(filepath):
    try:
        with open(filepath, 'r') as f:
            for line in f:
                words = ((line.strip()).split())
                if words:
                    first_word = words[0]
                    if first_word.isnumeric():
                        return first_word
    except Exception as e:
        return '0'
    else:
        return None


#Fucntion To Visit Menu Page.
@login_required(login_url="login")
def dish_page(request, *args, **kwargs):
    dish_id = kwargs.get('dish_id')
    dish = Dishes.objects.get(pk = dish_id)
    form = OrderForm()
    if request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            TABLE_PATH = request.POST.get('table_number')
            Cart.objects.create(
                customer = form.cleaned_data['customer'],
                ordered_dish = form.cleaned_data['ordered_dish'],
                quantity = form.cleaned_data['quantity'],
                total_amount = form.cleaned_data['total_amount'],
                table_number = returnTableNumber(TABLE_PATH),
            )
            return redirect('home')
        else:
            print("Invalid Form")
    else:
        form = OrderForm()
    customer = request.user
    count_order = Cart.objects.filter(customer=customer).filter(status="Pending").count()
    print(count_order)
    context = {}
    context['OrderCount'] = count_order
    context['dish'] = dish
    context['form'] = form
    return render(request , 'home/Dish_Page.html', context)