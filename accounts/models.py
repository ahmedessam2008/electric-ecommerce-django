from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  
  products_favorites = models.ManyToManyField(Product)
  address = models.CharField(max_length=100, null=True, blank=True)
  city = models.CharField(max_length=100, null=True, blank=True)
  country = models.CharField(max_length=100, null=True, blank=True)
  zipcode = models.CharField(max_length=100, null=True, blank=True)
  tel = models.CharField(max_length=100, null=True, blank=True)
  
  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name} From \"{self.city}\""