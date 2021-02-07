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