from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class lightUploadFile(forms.Form):
    patch_file = forms.FileField(required=False)

class fixture_patch(forms.Form):
    fixture = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    patch = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'class': 'form-control'}))