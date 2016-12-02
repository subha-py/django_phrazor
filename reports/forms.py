from django import forms

from reports.models import Report


EMPTY_NAME_ERROR='Please, enter a name for the report.'
EMPTY_TEXT_ERROR='Please, fill something.'

class ReportForm(forms.ModelForm):
    class Meta:
        model=Report
        fields=['name','file']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your file name',
            },),
        }
        error_messages = {
            'name': {'required': EMPTY_NAME_ERROR}
        }

    field_order = ('name','collection')



class DasboardForm(forms.ModelForm):
    class Meta:
        model=Report
        fields=['text']

        labels={
            'text':'Report Template'
        }
        widgets={
            'text':forms.Textarea(attrs={
                'placeholder':'Start typing here...',
                'rows':'10',
            })
        }

        error_messages={
            'text':{'required':EMPTY_TEXT_ERROR}
        }