from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

import yaml

#Logging to a speciefied file
import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/app/logs/settings.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

class SettingsForm(forms.Form):
    api_token = forms.CharField(max_length=1024, label='')
    category_mixers = forms.IntegerField(label='')
    category_microphones = forms.IntegerField(label='')
    category_di = forms.IntegerField(label='')
    category_stands = forms.IntegerField(label='')
    category_video_mixers = forms.IntegerField(label='')
    category_cameras = forms.IntegerField(label='')
    category_lights = forms.IntegerField(label='')