from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import yaml
import json
import requests

from .models import channel_lists

#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']



@login_required
def index(request):
    job_nr = request.GET.get('job', '')

    channel_lists_dict = channel_lists.objects.filter(projectID=job_nr)


    #Render index page
    return render(request, 'sound/index.html', {'channel_lists': channel_lists_dict})