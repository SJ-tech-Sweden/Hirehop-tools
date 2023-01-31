from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

import yaml
import json
import requests

from .models import channel_lists

#Logging to a speciefied file
import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/app/logs/sound.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']



@login_required
def index(request):
    job_nr = request.GET.get('job', '')

    channel_lists_dict = channel_lists.objects.filter(projectID=job_nr).values()

    logging.info(channel_lists_dict)

    if False:
        # example parameters
        parameters = {'job_nr': job_nr}

        # build the URL with the parameters and redirect
        url = '/sound/create_channellist?' + urlencode(parameters)
        return redirect(url)




    #Render index page
    return render(request, 'sound/index.html', {'channel_lists': channel_lists_dict})

@login_required
def create_channellist(request):
    job_nr = request.GET.get('job', '')

    #channel_lists_dict = channel_lists.objects.filter(projectID=job_nr)


    #Render index page
    return render(request, 'sound/create_channellist.html', {'job': job_nr})
