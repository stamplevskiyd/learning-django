from django.urls import path

from .views import *

urlpatterns = [
    path('', cars_list, name='cars_list_url'),
    path('days/', days_list, name='days_list_url'),
    path('car/create', CarCreate.as_view(), name='car_create_url'),
    path('car/<str:slug>', CarDetail.as_view(), name='car_detail_url'),
    path('day/create', DayCreate.as_view(), name='day_create_url'),
    path('day/<str:slug>', DayDetail.as_view(), name='day_detail_url'),
]
