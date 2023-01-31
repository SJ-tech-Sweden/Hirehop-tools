from django.urls import path

from . import views

urlpatterns = [
    path('new_job', views.new_job, name='new_job'),
    path('invoice_created', views.invoice_created, name='invoice_created'),
]