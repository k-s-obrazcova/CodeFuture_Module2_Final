from .views import *
from django.urls import path, include

urlpatterns = [
    path('product/all/', list_product, name='list_product'),
    path('product/all-filter/', list_product_with_filter, name='list_product_filter'),
    path('product/one-filter/', get_one_filter_product, name='one_filter_product'),
    path('product/more-filter/', get_more_filter_product, name='more_filter_product'),
    path('product/detail/<int:id>/', get_one_product, name='one_product_info'),
]