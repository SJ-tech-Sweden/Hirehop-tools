from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .forms import lightUploadFile

import os

import yaml
import json
import requests


#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']
light_file_upload_path = config['files']['light_path']



@login_required
def index(request):
    job_nr = request.GET.get('job', '')

    form = lightUploadFile()

    if request.method == 'POST':
        form = lightUploadFile(request.POST)
        if form.is_valid():
            request_file = request.FILES['patch_file'] if 'patch_file' in request.FILES else None
            cd = form.cleaned_data
            if request_file:
                fs = FileSystemStorage()

                path_url = "{}/{}/{}".format(light_file_upload_path, job_nr, request.FILES['patch_file'].name)

                try:
                    os.mkdir(os.path.join(light_file_upload_path, job_nr))
                except:
                    pass


    #Render index page
    return render(request, 'light/index.html', {'job': job_nr})