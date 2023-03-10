from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import date
from datetime import datetime

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.utilities.move_copy_util import MoveCopyUtil
from office365.sharepoint.files.file import File

from urllib.parse import quote

import yaml
import json

#Logging to a speciefied file
import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/app/logs/webhook.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']

#Sharepoint config
sharepoint_user = config['sharepoint']['username']
sharepoint_password = config['sharepoint']['password']
sharepoint_site = config['sharepoint']['site']
sharepoint_library = config['sharepoint']['document_library']
sharepoint_template_folder = config['sharepoint']['template_folder']


# Authenticate to SharePoint
client_credentials = UserCredential(sharepoint_user, sharepoint_password)

# Connect to the SharePoint site
client = ClientContext(sharepoint_site).with_credentials(client_credentials)



@csrf_exempt
def new_job(request):
    if request.method == 'POST':
        data = request.POST.dict()
        data_raw = request.body
        data_json = json.loads(request.body)

        job_data = data_json['data']
        job_name = job_data['JOB_NAME']

        job_year = job_data['JOB_DATE']
        job_year = datetime.strptime(job_year, "%Y-%m-%d %H:%M:%S").year

        create_sharepoint_folder = bool(job_data['CUSTOM_FIELDS']['sharepoint_project']['value'])

        if create_sharepoint_folder:
          
          
            source_folder_url = sharepoint_template_folder
            target_folder_url = "{}/{}/{}".format(sharepoint_library, job_year, job_name)
            
            source_folder = client.web.get_folder_by_server_relative_url(source_folder_url)

            #Make sure all folders exists
            target_folder = client.web.ensure_folder_path(target_folder_url).execute_query()

            #Copy folder with everythin in it
            target_folder = source_folder.copy_to_using_path(target_folder_url, True).get().execute_query()

            # Delete the newly created folder to only keep the copied folder
            client.web.get_folder_by_server_relative_path(target_folder_url).delete_object().execute_query()
            
            #Delete the last number from the name
            source_folder_url_rename = "{}1".format(target_folder_url)
            source_folder = client.web.get_folder_by_server_relative_url(source_folder_url_rename)
            source_folder.move_to(target_folder_url).execute_query()


        logging.info(data_json)
        print(create_sharepoint_folder)
        return JsonResponse({'status': 'success', 'data': data_json['data']})
    else:
        logging.info('No data')
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def invoice_created(request):
    if request.method == 'POST':
        data = request.POST.dict()
        data_raw = request.POST
        # process the webhook data here
        print(data)
        logging.info(data)
        logging.info(data_raw)
        return JsonResponse({'status': 'success'})
    else:
        logging.info('No data')
        return JsonResponse({'error': 'Invalid request method'})
