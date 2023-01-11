from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='List jobs'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_barcode/', views.checkout_barcode, name='checkout_barcode'),
]