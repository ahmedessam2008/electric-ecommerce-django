from django.urls import path
from . import views
urlpatterns = [
  path("store", views.store, name="store"),
  path('product/<int:id>', views.one_product, name="one_product"),
  path('search', views.advanced_search, name="advanced_search"),
]