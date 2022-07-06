from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from products.models import Product
import re
from django.contrib import auth

# Create your views here.
def signin(request):
  
  if request.method == "POST" and "signin" in request.POST:
    username = request.POST["username"]
    password = request.POST["password"]
    
    user = auth.authenticate(username=username, password=password)
    if user is not None:
      #الشرط دا علشان يعمل خروج لو قفلت المتصفح
      if "remember" not in request.POST:
        request.session.set_expiry(0)
      auth.login(request, user)
      # messages.success(request, "You Are Login")
    else:
      messages.error(request, "Username or password invalid")
    
    return redirect("signin")
  else:
    return render(request, "accounts/signin.html")


def logout(request):
  if request.user.is_authenticated:
    auth.logout(request)
    return redirect("index")
    
def signup(request):
  context = None
  if request.method == "POST" and "signup" in request.POST:
    firstname = None
    lastname = None
    username = None
    password = None
    email = None
    address = None
    city = None
    country = None
    zipcode = None
    tel = None
    is_added = None
    
    if "firstname" in request.POST: firstname= request.POST["firstname"]
    else: messages.error(request, "Error In First Name")
      
    if "lastname" in request.POST: lastname = request.POST["lastname"]
    else: messages.error(request, "Error In Last Name")
      
    if "username" in request.POST: username = request.POST["username"]
    else: messages.error(request, "Error In User Name")
      
    if "password" in request.POST: password = request.POST["password"]
    else: messages.error(request, "Error In Password")
      
    if "email" in request.POST: email = request.POST["email"]
    else: messages.error(request, "Error In Email")
      
    if "address" in request.POST: address = request.POST["address"]
    else: messages.error(request, "Error In Address")
      
    if "city" in request.POST: city = request.POST["city"]
    else: messages.error(request, "Error In City")
      
    if "country" in request.POST: country = request.POST["country"]
    else: messages.error(request, "Error In Country")
      
    if "zipcode" in request.POST: zipcode = request.POST["zipcode"]
    else: messages.error(request, "Error In Zip Code")
      
    if "tel" in request.POST: tel = request.POST["tel"]
    else: messages.error(request, "Error In Telephone")
    
    if firstname and lastname and username and password and email and address and city and country and zipcode and tel:
      if User.objects.filter(username=username).exists():
        messages.error(request, "User Is Token")
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, "Email is Exists")
        else:
          email_pattern = "^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$"
          if re.match(email_pattern, email):
            user = User.objects.create_user(
              first_name=firstname, last_name=lastname, email=email, username=username, password=password
            )
            user.save()
            # data 
            userprofile = UserProfile(
              user = user, address=address, city=city, country=country, zipcode=zipcode, tel=tel
            )
            userprofile.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            messages.success(request, f"User {username} is Added now")
            firstname = ''
            lastname = ''
            username = ''
            password = ''
            email = ''
            address = ''
            city = ''
            country = ''
            zipcode = ''
            tel = ''
            is_added = True
          else:
            messages.error(request, "Email Not Match The Email Pattern")
    else:
      messages.error(request, "Please Check Empty Fields")
      
    return render(request, "accounts/signup.html", {
      'firstname': firstname,
      'lastname': lastname,
      'username': username,
      'password': password,
      'email': email,
      'address': address,
      'city': city,
      'country': country,
      'zipcode': zipcode,
      'tel': tel,
      'is_added': is_added
    })
  else:
    return render(request, "accounts/signup.html", context)

def profile(request):

    # الجزء دا لما هيدوس علي الزرار يهبعت التعديلات

  if request.method == "POST" and "changeinfo" in request.POST:
    if request.user is not None and not request.user.is_anonymous:
      
      userprofile = UserProfile.objects.get(user=request.user)
      if request.POST["firstname"] and request.POST["lastname"] and request.POST["password"] and request.POST["email"] and request.POST["address"] and request.POST["city"] and request.POST["country"] and request.POST["zipcode"] and request.POST["tel"]:
        
        request.user.first_name = request.POST["firstname"]
        request.user.last_name = request.POST["lastname"]
        
        if not request.POST["password"].startswith("pbkdf2_sha256$"):
          request.user.set_password(request.POST["password"])
          
          
        request.user.email = request.POST["email"]
        userprofile.address = request.POST["address"]
        userprofile.city = request.POST["city"]
        userprofile.country = request.POST["country"]
        userprofile.zipcode = request.POST["zipcode"]
        userprofile.tel = request.POST["tel"]
        
        request.user.save()
        userprofile.save()
        messages.success(request, "Your Information is Updated")
      else:
        messages.error(request, "Please Check Empty Fields")
    return redirect("profile")
  
  else:
    # الجزء دا علشان لما ادخل علي البروفايل يجبلي بيانات المستخدم
    if request.user is not None:
      # لو اليوز موجود هبعت القيم دي لصفحة البروفايل علشان تظهرلي كقيمة للمدخلات
      context = None
      if not request.user.is_anonymous or request.user.id != None:
        userprofile = UserProfile.objects.get(user=request.user)
        context = {
          'firstname': request.user.first_name,
          'lastname': request.user.last_name,
          'username': request.user.username,
          'password': request.user.password,
          'email': request.user.email,
          'address': userprofile.address,
          'city': userprofile.city,
          'country': userprofile.country,
          'zipcode': userprofile.zipcode,
          'tel': userprofile.tel,
        }
      return render(request, "accounts/profileinfo.html", context)
    else:
      return redirect("profile")


def add_products_favorites(request, product_id):
  # add id to request علشان انا عاوز اجيب رقم المنتج
  if request.user.is_authenticated and not request.user.is_anonymous:
    # التحقق من المنتج موجود في المفضلة ام لا
    favorites_product_id = Product.objects.get(id=product_id)
    if UserProfile.objects.filter(user =request.user,  products_favorites=favorites_product_id).exists():
      messages.error(request, "The product is in Favorites")
    else:
      userprofile = UserProfile.objects.get(user=request.user)
      userprofile.products_favorites.add(favorites_product_id)
      messages.success(request, "Product Have in Favorietes")
  else:
    messages.error(request, "You Must Be Login")
  return redirect("/products/product/" + str(product_id))
  # return redirect(request.META.get('HTTP_REFERER'))


def show_products_favorites(request):
  context= {}
  if request.user.is_authenticated and not request.user.is_anonymous:
    userprofile = UserProfile.objects.get(user=request.user)
    favorites = userprofile.products_favorites.all()
    context= {
      "products": favorites,
    }
    return render(request, 'products/store.html', context)