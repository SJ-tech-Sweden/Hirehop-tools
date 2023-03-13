from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class lightUploadFile(forms.Form):
    patch_file = forms.FileField(required=False)