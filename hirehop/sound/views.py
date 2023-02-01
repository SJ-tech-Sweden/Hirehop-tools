from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

import yaml
import json
import requests
from urllib.parse import urlencode

from .models import channel_lists
from .forms import ChannelListsForm

#Logging to a speciefied file
import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/app/logs/sound.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')


#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']

def add_equipment(request, job_nr, id):
    url = "https://myhirehop.com/api/save_job.php?token={}".format(api_token)

    payload = {
        'job': job_nr,
        "items": {"b{}".format(id):1}
    }

    payload = json.dumps(payload)


    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    messages.info(response.text)

    mixer = json.loads(response.text)['items']['itms']

    messages.info(request, mixer)

    return mixer


def create_channellist_function(request, channellist_name, project_id, mixer_id):
    # create a channel_lists item
    channel_list = channel_lists.objects.create(Name=channellist_name, projectID=project_id, mixerID=mixer_id)

    url_list = "https://myhirehop.com/php_functions/check_in_list.php?token={}".format(api_token)

    job_nr = request.GET.get('job', '')
    job_name = request.GET.get('job_name', '')

    payload_list={
        'job': job_nr
    }
    headers_list={}

    response_list = requests.request("POST", url_list, headers=headers_list, data=payload_list)

    # create 24 channel_list_inputs
    for i in range(24):
        channel_list_input = channel_list_input.objects.create(channel_lists=channel_list, musician="Musician {}".format(i+1), 
                                                                notes="Input notes {}".format(i+1), instrument="Instrument {}".format(i+1),
                                                                stage_input="Stage Input {}".format(i+1), console_channel=i+1, 
                                                                mic_di="Mic DI {}".format(i+1))

    # create 12 channel_list_outputs
    for i in range(12):
        channel_list_output = channel_list_output.objects.create(channel_lists=channel_list, instrument="Instrument {}".format(i+1),
                                                                person="Person {}".format(i+1), output_type="Output Type {}".format(i+1),
                                                                console_output=i+1, notes="Output notes {}".format(i+1), mix="Mix {}".format(i+1))



@login_required
def index(request):
    job_nr = request.GET.get('job', '')

    channel_lists_dict = channel_lists.objects.filter(projectID=job_nr).values()
    channel_lists_list = list(channel_lists_dict)

    log_message = "Channellists: {}".format(channel_lists_list)

    if not channel_lists_list:
        logging.info('There are no channellists')

        parameters = {'job': job_nr}
        # build the URL with the parameters and redirect
        url = '/sound/create_channellist?' + urlencode(parameters)
        return redirect(url)

    logging.info(log_message)


    #Render index page
    return render(request, 'sound/index.html', {'channel_lists': channel_lists_list})

@login_required
def create_channellist(request):
    job_nr = request.GET.get('job', '')

    logging.info('Create new channellist')

    form = ChannelListsForm(initial={'projectID': job_nr})

    #If there is a POST-request
    if request.method == 'POST':
        form = ChannelListsForm(request.POST)
        #Check if form is valid
        if form.is_valid():
            cd = form.cleaned_data
            #update channellist with the form data
            logging.info(cd)
            messages.info(request, cd)

            mixer = add_equipment(request, cd.get('projectID'), cd.get('mixerID'))

            #Update the page
            return render(request, 'sound/create_channellist.html', {'job': job_nr, 'form': form})
        else:
            #If the form data is corupt it will show a message but since the form is only a optinon list and the options are always valid it shouldn´t happen
            messages.error(request, 'This shouldnt be able to happen...')
    #Before any POST-action render the page from this template

    #Render index page
    return render(request, 'sound/create_channellist.html', {'job': job_nr, 'form': form})
