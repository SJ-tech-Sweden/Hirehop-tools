from django import forms

import yaml
import json
import requests

import pandas as pd

from .models import channel_lists

#Logging to a speciefied file
import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/app/logs/sound.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

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

    logging.info(mixers)

    mixers_df = pd.DataFrame(mixers)

    mixers_list = mixers_df['cell'].tolist()

    #mixers_dict = {row['ID']: row['TITLE'] for index, row in df.iterrows()}

    logging.info(mixers_list)

    return "{ ilive: 134 }"

class ChannelListsForm(forms.Form):
    channel_list_name = forms.CharField(max_length=100)
    projectID = forms.CharField(max_length=30)
    mixerID = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mixers = get_mixers()
        mixer_choices = [(key, value) for key, value in mixers.items()]
        self.fields['mixerID'].choices = mixer_choices