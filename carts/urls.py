from django.urls import path

from products import urls
from . import views

urlpatterns = [
    path("mycart", views.cart_view, name="mycart"),
    path("add_cart/<int:id>/", views.cat_add, name="add_cart"),
    path("delete_cart/<int:id>/", views.delete_cart, name="delete_cart"),
    path("cart_item_remove/<int:id>/", views.cart_item_remove, name="cart_item_remove"),
    path("checkout", views.checkout, name="checkout"),
    # path('single_product/<int:id>/',views.single_product,name="single_product")
    path("apply_coupon",views.apply_coupon,name="apply_coupon"),
    path("carts/<int:id>/", views.adds_cart, name="adds_cart"),

]
