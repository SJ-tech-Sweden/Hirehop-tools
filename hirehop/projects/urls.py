from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='List jobs and projects'),
    path('settings', views.settings, name='Setup Hirehop connection'),

]