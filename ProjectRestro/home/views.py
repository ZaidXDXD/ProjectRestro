from django.shortcuts import render, redirect

from .forms import TagForm

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