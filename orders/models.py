from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from creditcards.models import CardExpiryField, CardNumberField, SecurityCodeField
# Create your models here.
class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date_added = models.DateTimeField()
  details = models.ManyToManyField(Product, through='OrderDetails')
  is_finished = models.BooleanField(default=False)
  total = 0
  items_count = 0
  def __str__(self):
    return f"User {self.user.username} & Order ID ({self.id})"

class OrderDetails(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  new_price = models.DecimalField(max_digits=15, decimal_places=2)
  quantity = models.IntegerField()
  
  def __str__(self):
    return f"User {self.order.user.username} Order ID ({self.order.id})"

  class Meta:
    ordering = ["-id"]
    
class Payment(models.Model):
  pyment_method = [
    ('paypal','paypal'),
    ('cod','cod'),
    ('credit','credit'),
    ('bank','bank'),
  ]
  order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=True)
  shipping_adress = models.CharField(max_length=150, null=False, blank=True)
  shipping_mobile = models.CharField(max_length=150, null=False, blank=True)
  pyment_method = models.CharField(max_length=100, choices=pyment_method)
  card_number  = CardNumberField()
  expired = CardExpiryField(default="12/22")
  security_code = SecurityCodeField()