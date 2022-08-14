from django.urls import URLPattern, path
from products import urls
from . import views
urlpatterns= [
    path("",views.invoice,name="invoice"),
    path("order_cancel/<int:id>/",views.order_cancel,name="order_cancel"),
    path("paypal",views.paypal,name="paypal"),
    path("cod",views.cod,name="cod"),
    # path("order-conforme",views.order_conforme,name="order_conforme"),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    # path('razopay', views.razopay, name='razopay'),
    # path('razopaypage', views.razopaypage, name='razopaypage'),
    path('success/', views.razorpay_sucess, name='success/'),
    path('payments', views.payments, name='payments'),
    path('order_complete', views.order_complete, name='order_complete'),
    path('product_return/<int:id>/', views.product_return, name='product_return'),
    path('product_order_cancel/<int:id>/', views.product_order_cancel, name='product_order_cancel'),
   
]