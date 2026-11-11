from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("sell/", views.sell_photo, name="sell_photo"),
    path("sell/details/", views.sell_details, name="sell_details"),
    path("my-listings/", views.my_listings, name="my_listings"),
    path("product/<int:pk>/edit/", views.edit_product, name="edit_product"),
    path("product/<int:pk>/delete/", views.delete_product, name="delete_product"),
    path("product/<int:pk>/sold/", views.mark_sold, name="mark_sold"),
]