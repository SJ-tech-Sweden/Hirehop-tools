from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

import yaml
import json
import requests

#Open configuration file
with open('hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']

# Create your views here.
def index(request):
    url = "https://myhirehop.com/frames/search_field_results.php?status=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8&rows=500&page=1&token={}".format(api_token)

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)

    jobs = json.loads(response.text)['rows']

    #messages.info(request, jobs)


    #Render index page
    return render(request, 'scanning/index.html', {'jobs': jobs})


def checkout(request):
    url = "https://myhirehop.com/php_functions/check_out_list.php?token={}".format(api_token)

    job_nr = request.GET.get('job', '')
    job_name = request.GET.get('job_name', '')

    payload={
        'job': job_nr
    }
    headers={}

    response = requests.request("POST", url, headers=headers, data=payload)

    items = json.loads(response.text)['rows']

    items_list = []

    for item in items:
        items_list.append(items[item])

    #messages.info(request, items_list)


    #Render index page
    return render(request, 'scanning/checkout.html', {'items': items_list, "job_name": job_name})


def checkout_barcode(request):
    job_nr = request.GET.get('job', '')
    barcode = request.GET.get('barcode', '')

    url = "https://myhirehop.com/php_functions/items_barcode_save.php?token={}".format(api_token)

    payload={'job': job_nr,
    'action': '1',
    'barcode': barcode,
    'parent': ''}

    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    messages.info(request, response.text)

    url_list = "https://myhirehop.com/php_functions/check_out_list.php?token={}".format(api_token)

    job_nr = request.GET.get('job', '')
    job_name = request.GET.get('job_name', '')

    payload_list={
        'job': job_nr
    }
    headers_list={}

    response_list = requests.request("POST", url_list, headers=headers_list, data=payload_list)

    items = json.loads(response_list.text)['rows']

    items_list = []

    for item in items:
        items_list.append(items[item])
    
    #return HttpResponse(status=204)
    return render(request, 'scanning/checkout.html', {'items': items_list, "job_name": job_name})


def checkin(request):
    url = "https://myhirehop.com/php_functions/check_all_in_list.php?token={}".format(api_token)


    payload={}
    headers={}

    response = requests.request("POST", url, headers=headers, data=payload)

    items = json.loads(response.text)['rows']

    items_list = []

    for item in items:
        items_list.append(items[item])

    #messages.info(request, items_list)


    #Render index page
    return render(request, 'scanning/checkin.html', {'items': items_list})


def checkin_barcode(request):
    barcode = job_nr = request.GET.get('barcode', '')
    
    return HttpResponse(status=204)
