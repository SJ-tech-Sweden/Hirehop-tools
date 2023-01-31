from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='List jobs'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_barcode/', views.checkout_barcode, name='checkout_barcode'),
    path('checkin/', views.checkin, name='checkin'),
    path('checkin_barcode/', views.checkin_barcode, name='checkin_barcode'),
]