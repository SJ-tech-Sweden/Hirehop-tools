from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import yaml
import json
import requests


#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']



@login_required
def index(request):
    job_nr = request.GET.get('job', '')


    #Render index page
    return render(request, 'sound/index.html', {'job': job_nr})