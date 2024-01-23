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
    api_token = forms.CharField(max_length=1024, label='', initial=config['hirehop']['api_token'], widget=forms.Textarea(attrs={"rows":"3"}))
    category_mixers = forms.IntegerField(label='', initial=config['hirehop']['categories']['mixers'])
    category_microphones = forms.IntegerField(label='', initial=config['hirehop']['categories']['microphones'])
    category_di = forms.IntegerField(label='', initial=config['hirehop']['categories']['di'])
    category_stands = forms.IntegerField(label='', initial=config['hirehop']['categories']['stands'])
    category_video_mixers = forms.IntegerField(label='', initial=config['hirehop']['categories']['video_mixers'])
    category_cameras = forms.IntegerField(label='', initial=config['hirehop']['categories']['cameras'])
    category_lights = forms.IntegerField(label='', initial=config['hirehop']['categories']['lights'])