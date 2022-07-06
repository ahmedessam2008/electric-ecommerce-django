from django.urls import path
from . import views
urlpatterns = [
  path("add_to_chart", views.add_to_chart, name="add_to_chart"),
  path("cart", views.cart, name="cart"),
  path("remove_orderdetails/<int:orderdetails_id>", views.remove_orderdetails, name="remove_orderdetails"),
  path('empty/<int:order_id>', views.empty_cart, name="empty_cart"),
  path("increase_qty/<int:orderdetails_id>", views.increase_qty, name="increase_qty"),
  path("decrease_qty/<int:orderdetails_id>", views.decrease_qty, name="decrease_qty"),
  path("payment", views.payment, name="payment"),
  path('show_orders', views.show_orders, name="show_orders")
]