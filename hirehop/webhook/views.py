from django.shortcuts import render
from django.http import JsonResponse

import yaml

#Logging to a speciefied file
import logging
#logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/app/logs/webhook.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']
# Create your views here.

def new_job(request):
    if request.method == 'POST':
        data = request.POST.dict()
        # process the webhook data here
        print(data)
        logging.info(info)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def invoice_created(request):
    if request.method == 'POST':
        data = request.POST.dict()
        # process the webhook data here
        print(data)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'})