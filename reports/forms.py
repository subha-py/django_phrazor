from django import forms

from reports.models import Report


EMPTY_NAME_ERROR='Please, enter a name for the report.'


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



