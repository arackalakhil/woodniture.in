from django.urls import path
from . import views

urlpatterns = [
    path("", views.signin_admins),
    path("admin_index", views.dashboard ,name ="admin_index"),
    path("admin_logout", views.signout_admin,name="admin_logout"),
    path("listproducts", views.list_products,name="listproducts"),
    path("data_table", views.user_data_table,name="data_table"),
    path("cat_products", views.category_products,name="cat_products"),
    path("block_user/<int:id>/", views.block_user,name="block_user"),
    # path('unblock_user/<int:id>/',views.update_user),
    path("delete_products/<int:id>/", views.delete_products,name="delete_products"),
    path("update_products/<int:id>/", views.update_products,name="update_products"),
    path("add_products", views.add_products,name="add_products"),
    path("add_categories", views.add_category,name="add_categories"),
    path("delete_categories/<int:id>/", views.delete_category,name="delete_categories"),
    path("update_categories/<int:id>/", views.update_category  ,name="update_categories"),
    path("order_management",views.order_management,name="order_management"),
    path("change_status/<int:id>/",views.change_status,name="change_status"),
    path("add_product_offer",views.add_product_offer,name="add_product_offer"),
    path("block_product_offer/<int:id>/", views.block_product_offer,name="block_product_offer"),
    path("delete_product_offers/<int:id>/",views.delete_product_offers,name="delete_product_offers"),
    path("product_offer_view",views.product_offer_view,name="product_offer_view"),
    path("edit_product_offer/<int:id>/",views.edit_product_offer,name="edit_product_offer"),


    path("add_category_offer",views.add_category_offer,name="add_category_offer"),
    path("block_category_offer/<int:id>/", views.block_category_offer,name="block_category_offer"),
    path("delete_category_offers/<int:id>/",views.delete_category_offers,name="delete_category_offers"),
    path("category_offer_view",views.category_offer_view,name="category_offer_view"),
    path("edit_category_offer/<int:id>/",views.edit_category_offer,name="edit_category_offer"),


    # path("orderdetails",views.orderdetails,name="orderdetails"),
    path("product_order_management/<int:id>/",views.product_order_management,name="product_order_management"),
    path("product_change_status/<int:id>/",views.product_change_status,name="product_change_status"),
    path("view_coupon",views.view_coupon,name="view_coupon"),
    path("add_coupon",views.add_coupon,name="add_coupon"),
    path("block_coupon/<int:id>/", views.block_coupon,name="block_coupon"),
    path("delete_coupon/<int:id>/",views.delete_coupon,name="delete_coupon"),

    path("salesreport",views.salesreport,name="salesreport"),
    path("monthly_report/<int:date>/",views.monthly_report,name="monthly_report"),
    # path("monthly_report/<int:id>/",views.monthly_report,name="monthly_report"),
    path("yearly_report/<int:date>/",views.yearly_report,name="yearly_report"),

    path("date_range",views.date_range,name="date_range"),
    path("view_banner",views.view_banner,name="view_banner"),
    path("adds_banners",views.adds_banners,name="adds_banners"),
    path("delete_banner/<int:id>/", views.delete_banner,name="delete_banner"),
    path("update_banner/<int:id>/",views.update_banner,name="update_banner"),
    path("block_banner/<int:id>/", views.block_banner,name="block_banner"),
    path("user_search", views.user_search,name="user_search"),


]
