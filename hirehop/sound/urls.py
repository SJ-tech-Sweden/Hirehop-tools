from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='List channellists'),
    path('create_channellist', views.create_channellist, name='Create channellist'),
    path('channellist', views.edit_channellist, name='Edit channellist'),
    path("channel_list_inputs/<str:pk>/update/", views.channel_list_input_update, name="sound_channel_list_inputs_update"),

]