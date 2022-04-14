from django.urls import path

from .views import *

urlpatterns = [
    path('', cars_list, name='cars_list_url'),
    path('cars/', cars_list, name='cars_list_url'),  # по дефолту пусть открывается страница с машинами
    path('days/', days_list, name='days_list_url'),
    path('months/', months_list, name='months_list_url'),
    path('car/create', CarCreate.as_view(), name='car_create_url'),
    path('car/<str:slug>', CarDetail.as_view(), name='car_detail_url'),
    path('day/create', DayCreate.as_view(), name='day_create_url'),
    path('day/<str:slug>', DayDetail.as_view(), name='day_detail_url'),
    path('month/create', MonthCreate.as_view(), name='month_create_url'),
    path('month/<str:slug>', MonthDetail.as_view(), name='month_detail_url'),
]
