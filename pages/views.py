from django.shortcuts import render
from products.models import Product
# Create your views here.

def index(request):
  context = None
  products = Product.objects.all()
  context = {
      "products": products,
  }
  return render(request, "pages/index.html", context)