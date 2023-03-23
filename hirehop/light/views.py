from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .forms import lightUploadFile

from sound.views import add_equipment

import os

import yaml
import csv
import json
import requests

#Logging to a speciefied file
import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/app/logs/light.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')


#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']
light_file_upload_path = config['files']['light_path']
light_category = config['hirehop']['categories']['lights']


def handle_uploaded_file(f, file_path):
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def get_lights():
    url = "https://myhirehop.com/modules/stock/list.php?rows=400&page=1&token={}&_search=true&head={}".format(api_token, light_category)

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)

    lights = {}

    try:
        lights = json.loads(response.text)['rows']
    except:
        lights = {}

    logging.info(lights)
    logging.info('---------------')


    lights_result = [{"display": item['cell']['TITLE'], "value": item['id']} for item in lights]


    logging.info('--- Result ---')
    logging.info(lights_result)

    return lights_result


@login_required
def index(request):
    job_nr = request.GET.get('job', '')

    fixture_list = []
    hirehop_lights = []

    form = lightUploadFile()

    table_sent = False

    if request.method == 'POST':
        form = lightUploadFile(request.POST)

        if "submit_upload" in request.POST:
            if form.is_valid():
                request_file = request.FILES['patch_file'] if 'patch_file' in request.FILES else None
                cd = form.cleaned_data
                if request_file:
                    fs = FileSystemStorage()

                    path_url = "{}/{}/{}".format(light_file_upload_path, job_nr, request.FILES['patch_file'].name)

                    hirehop_lights = get_lights()

                    try:
                        os.mkdir(os.path.join(light_file_upload_path, job_nr))
                    except:
                        pass

                    handle_uploaded_file(request.FILES['patch_file'], path_url)

                    file_name, file_extension = os.path.splitext(request_file.name)
                    if file_extension.lower() == '.csv':
                        with open(path_url, 'r') as csvfile:
                            reader = csv.DictReader(csvfile)
                            fixture_list = []
                            for row in reader:
                                fixture_list.append(row)
                        #messages.success(request, fixture_list)


                        
                            
                    elif file_extension.lower() == '.show.gz':
                        pass
                    messages.success(request, 'File uploaded')
                    table_sent = True

        elif "submit_fixture_list" in request.POST:
            
            fixture_list_to_hirehop = request.POST.getlist('form-fixture')
            messages.info(request, fixture_list_to_hirehop)
            for fixture in fixture_list_to_hirehop:
                if fixture != 0:
                    messages.info(request, fixture)
                    add_equipment(request, job_nr, fixture)




    #Render index page
    return render(request, 'light/index.html', {'form': form, 'job': job_nr, 'table_sent': table_sent, 'fixtures_list': fixture_list, 'hirehop_lights': hirehop_lights})