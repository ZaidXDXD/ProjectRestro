import base64
import json
import os

import cv2
import requests
from django.conf import settings
from django.contrib import messages
from django.core import files
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import (
    TagForm,
    DishesForm, 
    DishesIconImageForm, 
    DishesMajorImageForm,
)
from .models import (
    Tag, 
    Dishes,
)


def home(request):
    return render(request, 'home/home.html')


# View For Tags
def tagpage(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addDish')
    else:
        form = TagForm()
    return render(request, 'home/tag.html', {'form':form})

# View For Add Dish
def adddish(request):
    tags = Tag.objects.all().order_by('name')
    if request.method == "POST":
        form = DishesForm(request.POST)
        if form.is_valid():
            dish = form.save()
            return redirect('addIconImage', dish.pk )
    else:
        form = DishesForm()
    return render(request, 'home/NewDish.html', {'tags' : tags, "form" : form})


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
            imageString = request.POST.get("image")
            url = save_temp_icon_image_from_base64String(imageString, dish)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get('cropX'))))
            cropY = int(float(str(request.POST.get('cropY'))))
            cropWidth = int(float(str(request.POST.get('cropWidth'))))
            cropHeight = int(float(str(request.POST.get('cropHeight'))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

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
def add_dish_image_icon(request, *args, **kwargs):
    dish_id = kwargs.get('dish_id')
    dish_profile = Dishes.objects.get(pk=dish_id)
    context = {}
    context['dish'] = dish_profile
    if request.POST:
        form = DishesIconImageForm(request.POST, request.FILES, instance=dish_profile)
        if form.is_valid():
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
            imageString = request.POST.get("image")
            url = save_temp_major_image_from_base64String(imageString, dish)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get('cropX'))))
            cropY = int(float(str(request.POST.get('cropY'))))
            cropWidth = int(float(str(request.POST.get('cropWidth'))))
            cropHeight = int(float(str(request.POST.get('cropHeight'))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

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
def add_dish_image_major(request, *args, **kwargs):
    dish_id = kwargs.get('dish_id')
    dish_profile = Dishes.objects.get(pk=dish_id)
    context = {}
    context['dish'] = dish_profile
    if request.POST:
        form = DishesMajorImageForm(request.POST, request.FILES, instance=dish_profile)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = DishesMajorImageForm(request.POST, instance=dish_profile,
                initial={
                    "id" : dish_profile.id,
                    'major_image': dish_profile.major_image,
                })
            context['form'] = form

    else:
        form = DishesMajorImageForm(
            initial={
                    "id" : dish_profile.id,
                    'major_image': dish_profile.major_image,
                }
        )
        context['form'] = form
    
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'home/Add_New_Dish_Major_Image.html', context)