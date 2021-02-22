from django.shortcuts import render,redirect
from .models import Dishes, customer, order
from django.views import View
# Create your views here.
class Index(View):
    def post(self, request):
        dish = request.POST.get('dish')
        cart = request.session.get('cart')
        remove =request.POST.get('remove')
        if cart:
            quantity = cart.get(dish)
            if quantity:
                if remove == "True":
                    if quantity <= 1:
                        cart.pop(dish)
                    else :
                        cart[dish] = quantity - 1
                elif remove == "False":    
                    cart[dish] = quantity + 1
            else:
                cart[dish] = 1
        else:
            cart = {}
            cart[dish] = 1
        request.session['cart'] = cart
        return redirect('/')
    
    def get(self, request):
        cart = request.session.get('cart')
        if cart is None:
            request.session['cart'] = {}
        dish = Dishes.objects.all()
        return render(request, 'index.html',{'dishes': dish}) 


class Cart(View):
    def get(self, request):
        Customer_detail = customer.objects.get(id = request.session['Customer'])
        cart = request.session.get('cart')
        ids = list(cart.keys())
        sum = 0
        error_message = None
        dish_detail = Dishes.objects.filter(id__in = ids)
        for dish in dish_detail:
            instock = dish.stock - cart[str(dish.id)] >= 0
            if not instock:
                error_message = "We are Sorry, "+dish.name+" are out of Stock"
                return render(request, 'cart.html', {'dishes': dish_detail, 'Customer': Customer_detail,'error': error_message})
        for dish in dish_detail:
            sum += dish.price * cart[str(dish.id)]
        if sum < 300:
            error_message = "Minimum Order limit of Rs 300"
        return render(request, 'cart.html', {'dishes': dish_detail, 'Customer': Customer_detail, 'error': error_message})
    def post(self, request):
        dish = request.POST.get('dish')
        cart = request.session.get('cart')
        remove =request.POST.get('remove')
        quantity = cart.get(dish)
        if remove == "True":
            if quantity <= 1:
                cart.pop(dish)
            else:
                cart[dish] = quantity - 1
        elif remove == "False":    
            cart[dish] = quantity + 1
        request.session['cart'] = cart
        return redirect('cart')

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phoneno = request.POST.get('phoneno')
        Customer = request.session['Customer']
        cart = request.session.get('cart')
        ids = list(cart.keys())
        dishes = Dishes.objects.filter(id__in = ids)

        

        for dish in dishes:
            Order = order(Customer = customer(id = Customer), Dish = dish, address = address, phoneno = phoneno, quantity= cart[str(dish.id)], price = dish.price)
            Order.save()
            dish.stock = dish.stock - cart[str(dish.id)]
            dish.save()

        request.session['cart'] = {}
        return redirect('cart')

class Orders(View):
    def get(self, request):
        Customer_id = request.session.get('Customer')
        orders = order.objects.filter(Customer = Customer_id).order_by('-date')
        return render(request, 'orders.html', {'orders':orders})


def stock(request):
    if (request.method == "POST"):
        id =  request.POST.get('dish')
        remove = request.POST.get('remove')
        dishes = Dishes.objects.filter(id = id)
        for dish in dishes:
            if (remove == "True" and dish.stock > 0):
                dish.stock -= 1 
            elif (remove == "False" ):
                dish.stock += 1
            dish.save()
        return redirect('stock')

    else:
        dish_detail = Dishes.objects.all()
        return render(request, 'stock.html', {'dishes': dish_detail})

def sales(request):
    orders = order.objects.all()
    monthly_sum = [0,0,0,0,0,0,0,0,0,0,0,0]
    Total = 0
    for o in orders:
        date = str(o.date)
        if (date[5:7] == "01") and o.payment_status and o.completed:
            monthly_sum[0] += o.price * o.quantity 
        elif (date[5:7] == "02") and o.payment_status and o.completed:
            monthly_sum[1] += o.price * o.quantity 
        elif (date[5:7] == "03") and o.payment_status and o.completed:
            monthly_sum[2] += o.price * o.quantity 
        elif (date[5:7] == "04") and o.payment_status and o.completed:
            monthly_sum[3] += o.price * o.quantity 
        elif (date[5:7] == "05") and o.payment_status and o.completed:
            monthly_sum[4] += o.price * o.quantity 
        elif (date[5:7] == "06") and o.payment_status and o.completed:
            monthly_sum[5] += o.price * o.quantity 
        elif (date[5:7] == "07") and o.payment_status and o.completed:
            monthly_sum[6] += o.price * o.quantity 
        elif (date[5:7] == "08") and o.payment_status and o.completed:
            monthly_sum[7] += o.price * o.quantity 
        elif (date[5:7] == "09") and o.payment_status and o.completed:
            monthly_sum[8] += o.price * o.quantity 
        elif (date[5:7] == "10") and o.payment_status and o.completed:
            monthly_sum[9] += o.price * o.quantity 
        elif (date[5:7] == "11") and o.payment_status and o.completed:
            monthly_sum[10] += o.price * o.quantity 
        elif (date[5:7] == "12") and o.payment_status and o.completed:
            monthly_sum[11] += o.price * o.quantity
    for sum in monthly_sum:    
        Total += sum 
    return render(request, 'sales.html', {'sums':monthly_sum, 'total':Total})

