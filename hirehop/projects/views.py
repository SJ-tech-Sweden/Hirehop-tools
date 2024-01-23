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
    url = "https://myhirehop.com/frames/search_field_results.php?status=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8&rows=500&page=1&token={}".format(api_token)

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)

    jobs = {}

    try:
        jobs = json.loads(response.text)['rows']
    except:
        jobs = {}


    #Render index page
    return render(request, 'projects/index.html', {'jobs': jobs})

@login_required
def settings(request):

    #Render index page
    return render(request, 'projects/settings.html', {'config': config})