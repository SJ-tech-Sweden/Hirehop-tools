from django.contrib import admin

from .models import channel_lists, channel_list_input, channel_list_output

admin.site.register(channel_lists)
admin.site.register(channel_list_input)
admin.site.register(channel_list_output)
