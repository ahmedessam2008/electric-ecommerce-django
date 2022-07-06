from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
  list_display = ['title', 'brand', 'category', 'color', 'new_price', 'is_active', 'rating']
  list_display_links = ['title', 'new_price']
  list_editable = ['brand', 'is_active', 'category']
  search_fields = ['title']
  list_filter = ['category', 'color']
  
admin.site.register(Product, ProductAdmin)

admin.site.site_header = "Electric"
admin.site.site_title = "Electric | Admin"