from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import yaml

#Logging to a speciefied file
import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/app/logs/webhook.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']
# Create your views here.


@csrf_exempt
def new_job(request):
    if request.method == 'POST':
        data = request.POST.dict()
        data_raw = request.body
        # process the webhook data here
        print(data)
        logging.info(data)
        logging.info(data_raw)
        return JsonResponse({'status': 'success'})
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