from .models import Product
from .forms import ModelForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from accounts.models import UserProfile
from orders.models import Order, OrderDetails

def product_counts(request):
  context = {}
  products = Product.objects.all()
  labtop_count = products.filter(category='labtops').count()
  smartphones_count = products.filter(category='smartphones').count()
  lcd_count = products.filter(category='lcd').count()
  cameras_count = products.filter(category='cameras').count()
  accessories_count = products.filter(category='accessories').count()
  
  toshiba_count = products.filter(brand="toshiba").count()
  samsung_count = products.filter(brand="samsung").count()
  lg_count = products.filter(brand="lg").count()
  oppo_count = products.filter(brand="oppo").count()
  hawui_count = products.filter(brand="hawui").count()
  tornado_count = products.filter(brand="tornado").count()
  
  category_list = Product.category_list
  brand_list = Product.brands_list
  context = {
    "products": products,
    "labtops": labtop_count,
    "smartphones": smartphones_count,
    'lcd': lcd_count,
    'cameras': cameras_count,
    'accessories': accessories_count,
    'toshiba': toshiba_count,
    'samsung': samsung_count,
    'lg': lg_count,
    'oppo': oppo_count,
    'hawui': hawui_count,
    'tornado': tornado_count,
    'category_list': category_list,
    "brand_list": brand_list,
    "model_form": ModelForm,
  }
  return context
  
  
def userinfo(request):
  context= {}
  if request.user is not None:
    
    if not request.user.is_anonymous:
      userprofile = UserProfile.objects.get(user=request.user)
      context = {
        'address': userprofile.address,
        'city': userprofile.city,
        'country': userprofile.country,
        'zipcode': userprofile.zipcode,
        'tel': userprofile.tel,
      }
  return context

def cardinfo(request):
  context = {}
  if request.user.is_authenticated and not request.user.is_anonymous:
    order = Order.objects.all().filter(user=request.user, is_finished=False)
    if order:
      order = Order.objects.get(user=request.user, is_finished=False)
      orderdetails = OrderDetails.objects.all().filter(order=order)
      total = 0
      for sub in orderdetails:
        total += sub.new_price * sub.quantity
      context = {
        'order': order,
        'orderdetails': orderdetails,
        'total': total,
      }
  return context