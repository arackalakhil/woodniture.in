
from django.urls import path
from .import views
urlpatterns = [
    path('',views.index_page, name="index_page"),
    path('table_list',views.table_list, name="table_list"),
    path('bed_list',views.bed_list, name="bed_list"),
    path('single_product/<int:id>/',views.single_product,name="single_product"),
    path('search/',views.search,name="search"),
    # path('latest_bed/',views.latest_bed,name="latest_bed"),

    # path('latest_table/',views.latest_table,name="latest_table"),


]