from django.urls import path
from . import views
urlpatterns = [
  path("signin", views.signin, name="signin"),
  path("signup", views.signup, name="signup"),
  path("profile", views.profile, name="profile"),
  path("logout", views.logout, name="logout"),
  path("products_favorites/<int:product_id>", views.add_products_favorites, name="products_favorites"),
  path("favorites", views.show_products_favorites, name="favorites"),
]