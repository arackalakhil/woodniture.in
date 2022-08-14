from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path("login-register", views.signin, name="login-register"),
    path("loginuser", views.signin, name="signin"),



    
    path("signup", views.signup, name="signup"),
    path("logout", views.signout, name="logout"),
    path("number_login", views.number_login,name="number_login"),
    path("otp-login/<int:phone_number>/", views.otp,name="otp_login"),
    path("add_address", views.add_address, name="add_address"),
    path("user_profile",views.user_profile,name="user_profile"),
    path("delete_address/<int:id>/",views.delete_address,name="delete_address"),
    path("edit_address/<int:id>/",views.edit_address,name="edit_address"),
    path("add_new_address", views.add_new_address, name="add_new_address"),
    path("user_order_details/<int:id>/",views.user_order_details,name="user_order_details"),  
    # path("user_wallet",views.user_wallet,name="user_wallet"),
    path("update_user/<int:id>/",views.update_user,name="update_user"),
    path("update_password/<int:id>",views.update_password,name="update_password"),
]
