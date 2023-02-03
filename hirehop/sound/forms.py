from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

import yaml
import json
import requests

from .models import channel_lists, channel_list_input, channel_list_output

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
    logging.info('---------------')


    mixers_result = [(item['id'], item['cell']['TITLE']) for item in mixers]

    #mixers_dict = {row['ID']: row['TITLE'] for index, row in df.iterrows()}


    logging.info('--- Result ---')
    logging.info(mixers_result)

    return mixers_result

class ChannelListsForm(ModelForm):
    Name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    projectID = forms.CharField(widget=forms.HiddenInput)
    mixerID = forms.ChoiceField(choices=(get_mixers()), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:

        model = channel_lists

        fields = ['Name', 'projectID', 'mixerID']

        widgets = {
            'projectID': forms.HiddenInput(),
        }


    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs.update(initial={'mixerID': instance.mixerID})
        super().__init__(*args, **kwargs)
