from django import forms
from .models import Tune, UserTune


class TuneForm(forms.ModelForm):
    class Meta:
        model = Tune
        fields = ('name', 'composer', 'key', 'genre')


class UserTuneForm(forms.ModelForm):
    class Meta:
        model = UserTune
        fields = ('notes', 'playonpiano', 'playonjamsession', 'playonstage', 'havesheet', 'sheet')

