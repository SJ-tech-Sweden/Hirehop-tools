from django.db import models
from django.urls import reverse

from django.utils import timezone

import uuid


class channel_lists(models.Model):

    # Fields
    Name = models.TextField(max_length=100)
    ID = models.AutoField(primary_key=True)
    projectID = models.CharField(max_length=30)
    mixerID = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("sound_channel_lists_detail", args=(self.ID,))

    def get_update_url(self):
        return reverse("sound_channel_lists_update", args=(self.ID,))



class channel_list_input(models.Model):

    # Fields
    ID = models.CharField(max_length=36, default=uuid.uuid4, editable=False, primary_key=True)
    musician = models.TextField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    notes = models.TextField(max_length=500, blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)
    instrument = models.TextField(max_length=100, blank=True, null=True)
    stage_input = models.TextField(max_length=100, blank=True, null=True)
    console_channel = models.IntegerField(blank=True, null=True)
    channel_list = models.ForeignKey(channel_lists, on_delete=models.CASCADE, default="0")
    mic_di = models.TextField(max_length=100, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("sound_channel_list_inputs_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("sound_channel_list_inputs_update", args=(self.pk,))



class channel_list_output(models.Model):

    # Fields
    ID = models.CharField(max_length=36, default=uuid.uuid4, editable=False, primary_key=True)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)
    instrument = models.TextField(max_length=100, blank=True, null=True)
    person = models.TextField(max_length=100, blank=True, null=True)
    output_type = models.TextField(max_length=100, blank=True, null=True)
    console_output = models.IntegerField(blank=True, null=True)
    notes = models.TextField(max_length=500, blank=True, null=True)
    channel_list = models.ForeignKey(channel_lists, on_delete=models.CASCADE, default="0")
    created = models.DateTimeField(default=timezone.now, editable=False)
    mix = models.TextField(max_length=100, blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("sound_channel_list_outputs_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("sound_channel_list_outputs_update", args=(self.pk,))

