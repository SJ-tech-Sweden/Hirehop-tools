from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='List channellists'),
    path('create_channellist', views.create_channellist, name='Create channellist'),
    path('edit_channellist', views.edit_channellist, name='Edit channellist'),

]