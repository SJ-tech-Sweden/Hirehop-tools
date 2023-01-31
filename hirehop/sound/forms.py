import yaml
import json
import requests

from .models import channel_lists

#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']
mixer_category = config['hirehop']['categories']['mixers']

def get_mixers():
    url = "https://myhirehop.com/modules/stock/list.php?rows=400&page=1&token={}&_search=true&head={}".format(api_token, mixer_category)

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)

    mixers = {}

    try:
        mixers = json.loads(response.text)['rows']
    except:
        mixers = {}

    return mixers
