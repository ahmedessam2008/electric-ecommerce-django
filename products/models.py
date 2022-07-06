from django.db import models
from datetime import datetime


# Create your models here.
class Product(models.Model):
  category_list = [
    ('labtops','labtops'),
    ('smartphones','smartphones'),
    ('lcd','lcd'),
    ('cameras','cameras'),
    ('accessories','accessories'),
  ]
  color_list = [
    ("red", "red"),
    ("green", "green"),
    ("blue", "blue"),
    ("black", "black"),
    ("selver", "selver"),
    ("red", "red"),
  ]
  brands_list = [
    ("toshiba", "toshiba"),
    ("samsung", "samsung"),
    ("lg", "lg"),
    ("oppo", "oppo"),
    ("hawui", "hawui"),
    ("tornado", "tornado"),
  ]
  title = models.CharField(max_length=50, null=True, blank=True)
  brand = models.CharField(max_length=50, null=True, blank=True, choices=brands_list)
  label = models.CharField(max_length=50, null=True, blank=True)
  label_sale = models.CharField(max_length=50, null=True, blank=True)
  new_price = models.DecimalField(max_digits=9, decimal_places=2 ,null=True, blank=True)
  old_price = models.DecimalField(max_digits=9, decimal_places=2 ,null=True, blank=True)
  category = models.CharField(max_length=100, null=True, blank=True, choices=category_list)
  productimage0 = models.ImageField(upload_to="photos/%y/%m/%d", null=True, blank=True)
  productimage1 = models.ImageField(upload_to="photos/%y/%m/%d", null=True, blank=True)
  productimage2 = models.ImageField(upload_to="photos/%y/%m/%d", null=True, blank=True)
  productimage3 = models.ImageField(upload_to="photos/%y/%m/%d", null=True, blank=True)
  color = models.CharField(max_length=100, null=True, blank=True, choices=color_list)
  rating = models.IntegerField(null=True, blank=True)
  is_active = models.BooleanField(default=True)
  date_added = models.DateTimeField(default=datetime.now, null=True, blank=True)
  
  def __str__(self):
    return self.title
  
  class Meta:
    ordering = ["-date_added"]