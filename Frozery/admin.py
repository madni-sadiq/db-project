from django.contrib import admin
from .models import Dishes,customer, order
# Register your models here.
admin.site.register(Dishes)
admin.site.register(customer)
admin.site.register(order)