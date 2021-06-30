from django import forms
from django.core.validators import FileExtensionValidator

class EventForm(forms.Form):
    eventname = forms.CharField(max_length=50)
    eventlocation = forms.CharField(max_length=50)
    eventmessage = forms.CharField(max_length=1000)
    birthday = forms.CharField(max_length=50)
    file = forms.FileField()

class AddMediaForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'mp4', 'mkv'])])    