from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from orders.models import Order, Payment
from products.models import Product
from orders.models import OrderDetails
# Create your views here.
def add_to_chart(request):
  if request.user.is_authenticated and not request.user.is_anonymous and request.GET["qty"] and request.GET["pro_id"] and request.GET["qty"]:
    product_id = request.GET["pro_id"]
    qty = request.GET["qty"] 
    
       
    order = Order.objects.all().filter(user=request.user, is_finished=False)
    # لو المنتج مش موجود رقمة هيطلعني عالمنتجات الاساسية
    if not Product.objects.all().filter(id=product_id).exists():
      return redirect('products')
    product = Product.objects.get(id=product_id)
    if order:
      messages.success(request, "Have incomplated Order")
      old_order = Order.objects.get(user=request.user, is_finished=False)
      # الشرط دا علشان لو المنتج موجود قبل كده اجمعه عاللي زيه مش اضيفه جديد
      if OrderDetails.objects.all().filter(order=old_order, product=product).exists():
        orderdetails = OrderDetails.objects.get(order=old_order, product=product)
        orderdetails.quantity += int(qty)
        orderdetails.save()
      else:
        # لو المنتج مش موجود هيضيف اوردر جديد
        orderdetails = OrderDetails.objects.create(
          order=old_order, product=product, new_price=str(product.new_price), quantity=qty
        )
        
    else:
      # انشاء اوردر جديد 
      new_order = Order()
      new_order.user = request.user
      new_order.date_added = timezone.now()
      new_order.is_finished = False
      new_order.save()
      orderdetails = OrderDetails.objects.create(
        order=new_order, product=product, new_price=str(product.new_price), quantity=qty
      )
      messages.success(request, "New Order")
      
    return redirect("/products/product/" + str(request.GET["pro_id"]))
  else:
    if 'pro_id' in request.GET:
      messages.error(request, 'You must be Login')
      return redirect(f"/products/product/{request.GET['pro_id']}")
    else:
      return redirect("store")

def cart(request):
  context = {}
  if request.user.is_authenticated and not request.user.is_anonymous:
    # order = Order.objects.all().filter(user=request.user, is_finished=False)
    if Order.objects.all().filter(user=request.user, is_finished=False):
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
  return render(request, "orders/cart.html", context)

def remove_orderdetails(request, orderdetails_id):
  if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    orderdetails = OrderDetails.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id == request.user.id:
      orderdetails.delete()
  return redirect("cart")

def empty_cart(request, order_id):
  if request.user.is_authenticated and not request.user.is_anonymous and order_id:
    orders = Order.objects.all().filter(id=order_id)
    
    if orders.user.id == request.user.id:
      orders.delete()
  return redirect('cart')

def increase_qty(request, orderdetails_id):
  if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    orderdetails = OrderDetails.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id == request.user.id:
      orderdetails.quantity += 1
      orderdetails.save()
  return redirect("cart")

def decrease_qty(request, orderdetails_id):
  if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    orderdetails = OrderDetails.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id == request.user.id:
      orderdetails.quantity -= 1
      orderdetails.save()
  return redirect("cart")

def payment(request):
  context= {}
  address = None
  tel = None
  payment = None
  card_number = None
  expired = None
  security_code = None
  is_added = None
    
  if request.user.is_authenticated and not request.user.is_anonymous:
    
    if request.method == "POST" and "paymentbtn" in request.POST and 'address' in request.POST and 'tel' in request.POST and 'payment' in request.POST:
      address = request.POST['address']
      tel = request.POST['tel']
      payment = request.POST['payment']
      card_number = request.POST["card_number"]
      expired = request.POST["expired"]
      security_code = request.POST["security_code"]
      
      if Order.objects.all().filter(user=request.user,is_finished=False):
        order = Order.objects.get(user=request.user, is_finished=False)
      
      if address and tel and payment == "paypal":
        payment = Payment(order=order, shipping_adress=address, shipping_mobile=tel, pyment_method=payment)
        payment.save()
        order.is_finished = True
        order.save()
        messages.success(request, f"{payment} Ship Complated ")
      
      elif address and tel and payment == "credit" and 'card_number' in request.POST and 'expired' in request.POST and 'security_code' in request.POST:
        
        if card_number and expired and security_code:
          payment = Payment(order=order, shipping_adress=address, shipping_mobile=tel, pyment_method=payment)
          payment.save()
          order.is_finished = True
          order.save()
          messages.success(request, "Credit Card Ship ")
        else:
          messages.success(request, f"{payment} Card Details Empty ")
        
      elif address and tel and payment == "bank":
        payment = Payment(order=order, shipping_adress=address, shipping_mobile=tel, pyment_method=payment)
        payment.save()
        order.is_finished = True
        order.save()
        messages.success(request, f"{payment} Ship ")

      else :
        messages.error(request, "empty Feilds")
  else:
    messages.error(request, "You Are Not Loggin from payment view")
  return render(request, 'orders/checkout.html', context)

def show_orders(request):
  context = {}
  all_orders = None
  if request.user.is_authenticated and not request.user.is_anonymous:
    all_orders = Order.objects.all().filter(user=request.user)
    for x in all_orders:
      order = Order.objects.get(id=x.id, user=request.user)
      orderdetails = OrderDetails.objects.all().filter(order=order)
      total = 0
      for sub in orderdetails:
        total += sub.new_price * sub.quantity
      x.total = total
      x.items_count = orderdetails.count
    context={
      'all_orders': all_orders,
    }
  else:
    messages.error(request, "You Are Not Loggin ")
  return render(request, 'orders/show_orders.html', context)