from django import template

register = template.Library()

@register.filter(name = 'is_in_cart')
def is_in_cart(dish, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == dish.id:
            return True
        
    return False


@register.filter(name = 'cart_quantity')
def cart_quantity(dish, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == dish.id:
            return cart[id]
    
@register.filter(name = 'dish_total')
def dish_total(dish, cart):
    return cart_quantity(dish, cart)*dish.price

@register.filter(name = 'cart_total')
def cart_total(dishes, cart):
    sum =0
    for item in dishes:
        sum += dish_total(item, cart)
    return sum

@register.filter(name = 'delivery')
def delivery(dishes, cart):
    sum = cart_total(dishes, cart)
    if sum < 2000:
        return 200
    else:
        return 0

@register.filter(name = 'total')
def total(dishes, cart):
    sum = cart_total(dishes, cart)
    Delivery = delivery(dishes, cart)
    return sum + Delivery
    