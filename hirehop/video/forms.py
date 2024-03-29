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
                    filename='/app/logs/video.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']
mixer_category = config['hirehop']['categories']['video_mixers']
camera_category = config['hirehop']['categories']['cameras']
stand_category = config['hirehop']['categories']['stands']

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


def get_cameras():
    url = "https://myhirehop.com/modules/stock/list.php?rows=400&page=1&token={}&_search=true&head={}".format(api_token, camera_category)

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)

    camera_default = [(0, "Camera")]

    result = camera_default

    cameras = {}

    try:
        cameras = json.loads(response.text)['rows']
    except:
        cameras = {}

    logging.info(cameras)
    logging.info('---------------')


    cameras_result = [(item['id'], item['cell']['TITLE']) for item in cameras]

    result += cameras_result


    logging.info('--- Result ---')
    logging.info(result)

    return result

def get_stands():
    url = "https://myhirehop.com/modules/stock/list.php?rows=400&page=1&token={}&_search=true&head={}".format(api_token, stand_category)

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)

    stand_default = [(0, "Stand")]

    result = stand_default

    stands = {}

    try:
        stands = json.loads(response.text)['rows']
    except:
        stands = {}

    logging.info(stands)
    logging.info('---------------')


    stands_result = [(item['id'], item['cell']['TITLE']) for item in stands]

    result += stands_result

    logging.info('--- Result ---')
    logging.info(result)

    return result

class ChannelListsForm(ModelForm):
    #ChannelListForm = forms.BooleanField(widget=forms.HiddenInput, initial=True)
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
    notes = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    console_channel = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    camera = forms.ChoiceField(choices=(get_cameras()), label='', widget=forms.Select(attrs={'class': 'form-select'}))
    stand = forms.ChoiceField(choices=(get_stands()), label='', widget=forms.Select(attrs={'class': 'form-select'}))
    ID = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = channel_list_input
        fields = [
            "console_channel",
            "camera",
            "stand",
            "notes",
        ]


class ChannelListOutputForm(forms.ModelForm):
    output_type_choices = [
        ('main', 'PGM'),
        ('aux', 'Aux')
    ]

    notes = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    console_output = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    output_type = forms.ChoiceField(choices=(output_type_choices), label='', widget=forms.Select(attrs={'class': 'form-select'}))
    ID = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = channel_list_output
        fields = [
            "console_output",
            "output_type",
            "notes",
        ]