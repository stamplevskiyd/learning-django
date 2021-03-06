from django.urls import path

from .views import *

urlpatterns = [
    path('', cars_list, name='cars_list_url'),
    path('amortization/<int:id>', AmortizationDetail.as_view(), name='amortization_detail_url'),
    path('amortization/<int:id>/delete', AmortizationDelete.as_view(), name='amortization_detail_url'),
    path('cars/', cars_list, name='cars_list_url'),  # по дефолту пусть открывается страница с машинами
    path('days/', days_list, name='days_list_url'),
    path('months/', months_list, name='months_list_url'),
    path('car/create', CarCreate.as_view(), name='car_create_url'),
    path('car/<int:id>', CarDetail.as_view(), name='car_detail_url'),
    path('car/<int:id>/add_day', DayCreate.as_view(), name='day_create_url'),
    path('car/<int:id>/add_amortization', AmortizationCreate.as_view(), name='amortization_create_url'),
    path('car/<int:id>/edit', CarEdit.as_view(), name='car_edit_url'),
    path('day/<int:id>', DayDetail.as_view(), name='day_detail_url'),
    path('day/<int:id>/edit', DayEdit.as_view(), name='day_edit_url'),
    path('month/<int:id>', MonthDetail.as_view(), name='month_detail_url'),
]
