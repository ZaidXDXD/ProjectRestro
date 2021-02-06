from django.shortcuts import redirect, render

from .forms import DishesForm, TagForm
from .models import Tag


def home(request):
    return render(request, 'home/home.html')


# View For Tags
def tagpage(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
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
            return redirect('home')
    else:
        form = DishesForm()
    return render(request, 'home/NewDish.html', {'tags' : tags, "form" : form})
