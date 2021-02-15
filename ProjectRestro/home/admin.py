from django.contrib import admin

from .models import Tag, Dishes, Order

admin.site.register(Tag)
admin.site.register(Dishes)
admin.site.register(Order)