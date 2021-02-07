from django.urls import path
from . import views
from Frozery.middlewares.auth_middleware import auth_middleware
urlpatterns = [
    path('', views.Index.as_view(), name = 'index'),
    path('cart',auth_middleware(views.Cart.as_view()), name = 'cart'),
    path('check-out', views.CheckOut.as_view(), name = 'checkout'),
    path('orders', auth_middleware(views.Orders.as_view()), name = 'orders')
]