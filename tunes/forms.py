from django import forms
from .models import Tune, UserTune
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, Column
from crispy_forms.bootstrap import FieldWithButtons


class TuneForm(forms.ModelForm):
    class Meta:
        model = Tune
        fields = ('name', 'composer', 'key', 'genre')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(

        )



class UserTuneForm(forms.ModelForm):
    class Meta:
        model = UserTune
        fields = ('notes', 'playonpiano', 'playonjamsession', 'playonstage', 'havesheet', 'sheet','public')
        labels = {
        "playonpiano": "I can play this on piano",
        'playonjamsession': 'I can play this on a jam-sesion',
        'playonstage': 'I can play this on stage',
        'havesheet': 'I have a sheet'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #crispy-form helper
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(

        )
        self.helper.add_input(Submit('submit', 'Submit'))


class UserTuneSearchForm(forms.ModelForm):
    q = forms.CharField(max_length=100, label='', required=False)
    class Meta:
        model = UserTune
        fields = ('playonpiano', 'playonjamsession', 'playonstage', 'havesheet')
        labels = {
        "playonpiano": "Piano",
        'playonjamsession': 'Jam',
        'playonstage': 'Stage',
        'havesheet': 'Sheet'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #crispy-form helper
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(


                FieldWithButtons(
                    Field('q',), Submit('', 'Search')),
                'playonpiano',
                'playonjamsession',
                'playonstage',
                'havesheet'

            
        )

class HomeSearchForm(forms.Form):
    q = forms.CharField(max_length=100, label='', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #crispy-form helper
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
                FieldWithButtons(
                    Field('q',), Submit('', 'Search')),
            )