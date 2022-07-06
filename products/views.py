from django.shortcuts import render
from .models import Product
from .forms import ModelForm
from django.core.paginator import Paginator


# Create your views here.
def store(request):

  search_products = Product.objects.all()
  context = None
  title = None
  brand = None
  label_sale = None
  new_price = None
  category = None
  color = None
  rating = None

  if "title" in request.GET:
    title = request.GET["title"]
    if title:
      search_products = search_products.filter(title__icontains=title)

    if "brand" in request.GET:
      brand = request.GET["brand"]
    if brand:
      search_products = search_products.filter(brand__icontains=brand)

    if 'label_sale' in request.GET:
      label_sale = request.GET["label_sale"]
    if label_sale:
      search_products = search_products.filter(label_sale__icontains=label_sale)

    if 'new_price' in request.GET:
      new_price = request.GET["new_price"]
    if new_price:
      search_products = search_products.filter(new_price__icontains=new_price)

    if "category" in request.GET:
      category = request.GET["category"]
    if category:
      search_products = search_products.filter(category__icontains=category)

    if "color" in request.GET:
      color = request.GET["color"]
    if color:
      search_products = search_products.filter(color__icontains=color)

    if "rating" in request.GET:
      rating = request.GET["rating"]
    if rating:
      search_products = search_products.filter(rating__icontains=rating)

  category_labtop = search_products.filter(category='labtops').count()
  category_list = Product.category_list
  brand_list = Product.brands_list

  paginator = Paginator(search_products, 9)  # Show 9 contacts per page.
  page_number = request.GET.get('page')
  search_products = paginator.get_page(page_number)

  context = {
      'category_list': category_list,
      "brand_list": brand_list,
      "labtops": category_labtop,
      "products": search_products,
  }
  return render(request, "products/store.html", context)


def one_product(request, id):
    products = Product.objects.all()
    one_product = Product.objects.get(id=id)
    related_products = products.filter(title__icontains=one_product.title)
    context = {
        "one_product": one_product,
        "related_products": related_products,
    }
    return render(request, "products/product.html", context)


def advanced_search(request):

    return render(request, "products/advanced_search.html")
