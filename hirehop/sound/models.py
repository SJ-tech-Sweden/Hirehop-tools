from django.db import models
from django.urls import reverse


class channel_lists(models.Model):

    # Fields
    Name = models.TextField(max_length=100)
    ID = models.AutoField(primary_key=True)
    projectID = models.CharField(max_length=30)
    mixerID = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("sound_channel_lists_detail", args=(self.ID,))

    def get_update_url(self):
        return reverse("sound_channel_lists_update", args=(self.ID,))



class channel_list_inputs(channel_lists):

    # Fields
    musician = models.TextField(max_length=100)
    #created = models.DateTimeField(auto_now_add=True, editable=False)
    notes = models.TextField(max_length=500)
    #last_updated = models.DateTimeField(auto_now=True, editable=False)
    instrument = models.TextField(max_length=100)
    stage_input = models.TextField(max_length=100)
    console_channel = models.IntegerField(blank=True, null=True)
    #channel_list = models.ForeignKey(channel_lists, on_delete=models.CASCADE)
    mic_di = models.TextField(max_length=100)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("sound_channel_list_inputs_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("sound_channel_list_inputs_update", args=(self.pk,))



class channel_list_outputs(channel_lists):

    # Fields
    #last_updated = models.DateTimeField(auto_now=True, editable=False)
    instrument = models.TextField(max_length=100)
    person = models.TextField(max_length=100)
    output_type = models.TextField(max_length=100)
    console_output = models.IntegerField(blank=True, null=True)
    notes = models.TextField(max_length=500)
    #channel_list = models.ForeignKey(channel_lists, on_delete=models.CASCADE)
    #created = models.DateTimeField(auto_now_add=True, editable=False)
    mix = models.TextField(max_length=100)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("sound_channel_list_outputs_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("sound_channel_list_outputs_update", args=(self.pk,))

