from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django import forms
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt



import yaml
import json
import requests
from urllib.parse import urlencode

from .models import channel_lists, channel_list_input, channel_list_output
from .forms import ChannelListsForm, ChannelListInputForm, ChannelListOutputForm

#Logging to a speciefied file
import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='/app/logs/sound.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')


#Open configuration file
with open('/app/hirehopScanning/config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

api_token = config['hirehop']['api_token']

def add_equipment(request, job_nr, id):
    url = "https://myhirehop.com/api/save_job.php?token={}".format(api_token)

    payload = {
        'job': job_nr,
        "items": {"b{}".format(id):1}
    }

    payload = json.dumps(payload)


    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    logging.debug(response.text)

    #messages.info(request, response.text)

    device = json.loads(response.text)['items']['itms']

    return device

def delete_equipment(request, job_nr, id):
    url_delete = "https://myhirehop.com/php_functions/items_delete.php?token={}".format(api_token)

    #Get id from job
    url_get_items = "https://myhirehop.com/frames/items_to_supply_list.php?token={}&job={}".format(api_token, job_nr)

    payload={}
    headers={}

    response_items = requests.request("GET", url_get_items, headers=headers, data=payload)

    json_items = json.loads(response_items.text)

    list_items = json_items['items']

    messages.info(request, list_items)

    for item in list_items:
        if item['LIST_ID'] == id:
            item_id = item['ID']
    messages.info(request, item_id)


    payload = {
        'job': job_nr,
        "items": {"c{}".format(item_id):1}
    }

    payload = json.dumps(payload)


    headers = {}

    response = requests.request("POST", url_delete, headers=headers, data=payload)

    logging.debug(response.text)

    messages.info(request, response.text)

    #device = json.loads(response.text)['items']['itms']

    return "deleted"

def get_job_data(request, job_nr):
    url = "https://myhirehop.com/api/job_data.php?token={}&job={}".format(api_token, job_nr)

    payload={}
    headers={}

    response = requests.request("GET", url, headers=headers, data=payload)

    job = json.loads(response.text)
    return job



def create_channellist_function(request, channellist_name, project_id, mixer_id, mixer):
    # create a channel_lists item
    channel_list = channel_lists.objects.create(Name=channellist_name, projectID=project_id, mixerID=mixer_id)


    inputs = int(mixer[0]['CUSTOM_FIELDS']['inputs']['value'])
    outputs = int(mixer[0]['CUSTOM_FIELDS']['outputs']['value'])

    # create channel_list_inputs
    for i in range(inputs):
        channel_list_input_1 = channel_list_input.objects.create(channel_list=channel_list, musician="Musician", 
                                                                notes="", instrument="Instrument",
                                                                stage_input="{}".format(i+1), console_channel=i+1, 
                                                                mic_di="", phantom_power=False)

    # create channel_list_outputs
    for i in range(outputs):
        channel_list_output_1 = channel_list_output.objects.create(channel_list=channel_list, instrument="Instrument",
                                                                person="Person", output_type="Output Type",
                                                                console_output=i+1, notes="Output notes", mix="Mix {}".format(i+1))



@login_required
def index(request):
    job_nr = request.GET.get('job', '')
    channel_list_id = request.GET.get('channel_list', '')
    action = request.GET.get('action', '')


    channel_lists_dict = channel_lists.objects.filter(projectID=job_nr).values()
    channel_lists_list = list(channel_lists_dict)

    log_message = "Channellists: {}".format(channel_lists_list)

    if action == 'delete':
        channel_lists.objects.filter(ID=channel_list_id).delete()
        channel_lists_dict = channel_lists.objects.filter(projectID=job_nr).values()
        channel_lists_list = list(channel_lists_dict)

    if action == 'new' or not channel_lists_list:

        parameters = {'job': job_nr}
        # build the URL with the parameters and redirect
        url = '/sound/create_channellist?' + urlencode(parameters)
        return redirect(url)

    logging.info(log_message)


    #Render index page
    return render(request, 'sound/index.html', {'channel_lists': channel_lists_list, 'job': job_nr})

@login_required
def create_channellist(request):
    job_nr = request.GET.get('job', '')

    logging.info('Create new channellist')

    form = ChannelListsForm(initial={'projectID': job_nr})

    #If there is a POST-request
    if request.method == 'POST':
        form = ChannelListsForm(request.POST)
        #Check if form is valid
        if form.is_valid():
            cd = form.cleaned_data
            #update channellist with the form data
            logging.info(cd)

            #messages.info(request, cd)

            mixer = add_equipment(request, cd.get('projectID'), cd.get('mixerID'))

            create_channellist_function(request, cd.get('Name'), cd.get('projectID'), cd.get('mixerID'), mixer)

            #Update the page
            parameters = {'job': job_nr}
            # build the URL with the parameters and redirect
            url = '/sound/?' + urlencode(parameters)
            return redirect(url)
        else:
            #If the form data is corupt it will show a message but since the form is only a optinon list and the options are always valid it shouldn´t happen
            messages.error(request, 'This shouldnt be able to happen...')
    #Before any POST-action render the page from this template

    #Render index page
    return render(request, 'sound/create_channellist.html', {'job': job_nr, 'form': form})


@login_required
def edit_channellist(request):
    job_nr = request.GET.get('job', '')
    channel_list_ID = request.GET.get('channel_list', '')

    job = get_job_data(request, job_nr)

    channel_lists_obj = get_object_or_404(channel_lists, ID=channel_list_ID)

    channel_list_inputs = channel_list_input.objects.filter(channel_list=channel_list_ID).order_by('console_channel')

    channel_list_outputs = channel_list_output.objects.filter(channel_list=channel_list_ID).order_by('console_output')

    ChannelListInputFormSet = forms.modelformset_factory(
        channel_list_input,
        form=ChannelListInputForm,
        extra=0,
        can_delete=True
    )

    ChannelListOutputFormSet = forms.modelformset_factory(
        channel_list_output,
        form=ChannelListOutputForm,
        extra=0,
        can_delete=True
    )

    # set prefix for each form in the queryset
    for i, channel_list_input_obj in enumerate(channel_list_inputs):
        channel_list_inputs[i].prefix = "{}".format(channel_list_input_obj.pk)

    # set prefix for each form in the queryset
    for i, channel_list_output_obj in enumerate(channel_list_outputs):
        channel_list_outputs[i].prefix = "{}".format(channel_list_output_obj.pk)

    formset_input = ChannelListInputFormSet(queryset=channel_list_inputs, data=request.POST or None)

    formset_output = ChannelListOutputFormSet(queryset=channel_list_outputs, data=request.POST or None)
    #formset = ChannelListInputForm(request.POST or None, job_nr=job, channel_list_ID=channel_list_ID)
    form = ChannelListsForm(instance=channel_lists_obj, initial={'job': job_nr, 'channel_list': channel_list_ID})




    logging.info('Edit channellist')

    if request.method == 'POST':
        

        if 'submit_channel_list_input_pk' in request.POST:
            pk = request.POST['submit_channel_list_input_pk']
            formset_input = ChannelListInputFormSet(queryset=channel_list_inputs, data=request.POST or None)
            channel_list_input_obj = get_object_or_404(channel_list_input, ID=pk)
            #messages.error(request, channel_list_input_obj.__dict__)
            #form_input = ChannelListInputForm(request.POST, instance=channel_list_input_obj)
            form_input = ChannelListInputForm(request.POST, instance=channel_list_input_obj, prefix="form-{}".format(pk))
            #messages.info(request, pk)
            #messages.error(request, form_input)
            #messages.error(request, request.POST)
            #messages.error(request, 'Formset: {}'.format(formset))
            #for formset_item in formset:
            #    messages.error(request, 'Form: {} --- {}'.format(formset_item, formset_item.instance))

            
            
            
            

            if form_input.is_valid():
                cd = form_input.cleaned_data
                input = channel_list_input.objects.get(ID=pk)
                #messages.info(request, job_nr)
                #messages.info(request, "Form content - {}".format(cd))
                #messages.info(request, "Channel-list_input_obj - {}".format(channel_list_input_obj.__dict__))
                #messages.info(request, "Input - {}".format(input.__dict__))
                #messages.info(request, cd.get("mic_di"))
                
                if cd.get("mic_di") != "0" and not input.mic_di == cd.get("mic_di"):
                    add_equipment(request, job_nr, cd.get('mic_di'))
                    if input.mic_di != "0":
                        messages.info(request, "Delete the old microphone from hirehop")
                        delete_equipment(request, job_nr, input.mic_di)
                    messages.info(request, "Add mic to hirehop, if you changed from another mic please delete the old microphone from hirehop")
                form_input.save()
                messages.success(request, 'Updating Channellist input')
                return redirect('/sound/channellist?channel_list={}&job={}'.format(channel_list_ID, job_nr))
            
            else:
                messages.error(request, 'Form data is not valid.')
                #messages.error(request, formset.data)
                #messages.error(request, form_input.data)
                messages.error(request, formset_input.errors)
                messages.error(request, form_input.errors)
                messages.error(request, form.errors)
                #for field, errors in formset.errors.items():
                    #for error in errors:
                        #messages.info(request, "{}: {}".format(field, error))
        
        elif 'submit_channel_list_output_pk' in request.POST:
            pk = request.POST['submit_channel_list_output_pk']
            formset_output = ChannelListOutputFormSet(queryset=channel_list_outputs, data=request.POST or None)
            channel_list_output_obj = get_object_or_404(channel_list_output, ID=pk)

            form_output = ChannelListOutputForm(request.POST, instance=channel_list_output_obj, prefix="form-{}".format(pk))


            
            
            
            

            if form_output.is_valid():
                cd = form_output.cleaned_data
                output = channel_list_output.objects.get(ID=pk)
                
                form_output.save()
                messages.success(request, 'Updating Channellist output')
                return redirect('/sound/channellist?channel_list={}&job={}'.format(channel_list_ID, job_nr))
            
            else:
                messages.error(request, 'Form data is not valid.')

                messages.error(request, formset_output.errors)
                messages.error(request, form_output.errors)
                messages.error(request, form.errors)



        else:
            # Update channel_lists data
            messages.info(request, 'Updating Channellist data')
            form = ChannelListsForm(request.POST, instance=channel_lists_obj)
            
            if form.is_valid():
                form.save()

                return redirect('/sound/channellist?channel_list={}&job={}'.format(channel_list_ID, job_nr))
            else:
                messages.error(request, 'Form data is not valid.')
                messages.error(request, form.data)

    else:
        # Display the forms
        form = ChannelListsForm(instance=channel_lists_obj, initial={'job': job_nr, 'channel_list': channel_list_ID})


    return render(request, 'sound/edit_channellist.html', {'job': job_nr, 'form': form, 'job_data': job, 'formset_input': formset_input, 'formset_output': formset_output, 'channel_list': channel_list_ID})

