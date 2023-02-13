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
mic_category = config['hirehop']['categories']['microphones']
di_category = config['hirehop']['categories']['di']

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


def get_mics():
    url = "https://myhirehop.com/modules/stock/list.php?rows=400&page=1&token={}&_search=true&head={}".format(api_token, mic_category)

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)

    mics = {}

    try:
        mics = json.loads(response.text)['rows']
    except:
        mics = {}

    logging.info(mics)
    logging.info('---------------')


    mics_result = [(item['id'], item['cell']['TITLE']) for item in mics]

    url = "https://myhirehop.com/modules/stock/list.php?rows=400&page=1&token={}&_search=true&head={}".format(api_token, di_category)

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)

    di = {}

    try:
        di = json.loads(response.text)['rows']
    except:
        di = {}

    logging.info(di)
    logging.info('---------------')


    di_result = [(item['id'], item['cell']['TITLE']) for item in di]

    



    mics_result += di_result

    logging.info('--- Result ---')
    logging.info(mics_result)

    return mics_result

class ChannelListsForm(ModelForm):
    #form_identifier = forms.CharField(widget=forms.HiddenInput(), initial="ChannelListForm")
    Name = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    projectID = forms.CharField(widget=forms.HiddenInput)
    #ID = forms.CharField(widget=forms.HiddenInput)
    mixerID = forms.ChoiceField(choices=(get_mixers()), label='', widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:

        model = channel_lists

        fields = ['Name', 'projectID','ID', 'mixerID']

        widgets = {
            'projectID': forms.HiddenInput(),
            'ID': forms.HiddenInput(),
        }


    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs.update(initial={'mixerID': instance.mixerID})
        super().__init__(*args, **kwargs)


class ChannelListInputForm(forms.ModelForm):
    #form_identifier = forms.CharField(widget=forms.HiddenInput(), initial="ChannelListInputForm")
    musician = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    instrument = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    stage_input = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    console_channel = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    mic_di = forms.ChoiceField(choices=(get_mics()), label='', widget=forms.Select(attrs={'class': 'form-select'}))
    channel_list = forms.CharField(widget=forms.HiddenInput)
    

    class Meta:
        model = channel_list_input
        fields = [
            "console_channel",
            "stage_input",
            "instrument",
            "mic_di",
            "musician",
            "notes",
            "channel_list",
        ]