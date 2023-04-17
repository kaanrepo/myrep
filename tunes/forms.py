from django import forms
from .models import Tune, UserTune, UserTuneList
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, Column
from crispy_forms.bootstrap import FieldWithButtons
from django.db.models import Q


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
        fields = ('notes', 'playonpiano', 'playonjamsession', 'playonstage', 'havesheet', 'sheet','public','lyrics')
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
        
class UserTuneListForm(forms.ModelForm):
    class Meta:
        model = UserTuneList
        fields = ('name', 'description', 'tunes')
 
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['tunes'].queryset = UserTune.objects.filter(Q(user=user) | Q(public=True))

        #crispy-form helper
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            'name',
            'description',
            'tunes',
            Submit('submit','Save')
        )

