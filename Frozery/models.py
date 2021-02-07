from django.db import models
import datetime

# Create your models here.
class Dishes(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    desc = models.TextField()
    offer = models.BooleanField(default=False)
    img = models.ImageField(upload_to = 'pics')
    stock = models.IntegerField(default = 0)

class customer(models.Model):
    first_name = models.CharField(max_length=15)
    Last_name = models.CharField(max_length=15)
    phoneno = models.CharField(max_length=11)
    addr = models.TextField()
    email = models.EmailField()
    password = models.CharField(max_length = 500)

class order(models.Model):
    cash_on_del = 'COD'
    jazzcash = 'JZC'
    easypaisa = 'EPS'
    payment_choices = [
        (cash_on_del, 'Cash On Delivery'),
        (jazzcash, 'Jazzcash'),
        (easypaisa, 'Easypaisa'),
    ]
    Customer = models.ForeignKey(customer, on_delete = models.CASCADE)
    Dish = models.ForeignKey(Dishes,  on_delete=models.CASCADE)
    quantity = models.IntegerField(default= 1)
    price = models.IntegerField()
    address = models.TextField()
    phoneno = models.CharField(max_length=11)
    date = models.DateTimeField(default = datetime.datetime.today)
    completed = models.BooleanField(default=False)
    payment_type = models.CharField(
        max_length=3,
        choices=payment_choices,
        default=cash_on_del,
    )
    payment_status = models.BooleanField(default=False)



    