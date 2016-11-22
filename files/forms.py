from django import forms

from files.models import File


EMPTY_NAME_ERROR='Please, enter a name for the file.'


class FileForm(forms.ModelForm):
    file=forms.FileField(label='Upload File')
    class Meta:
        model=File
        fields=['name','desc']

        labels = {
            'desc': 'Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your file name',
            },),
            'desc':forms.Textarea(attrs={
                'placeholder': 'A bit description of the file may be helpful to you later',
                'rows':5,
            }),
        }
        error_messages = {
            'name': {'required': EMPTY_NAME_ERROR}
        }

    field_order = ('name','desc','file')

    def clean_file(self):
        file=self.cleaned_data.get('file')
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('Only csv files are supported now')

        return file

    def save(self, for_user):
        self.instance.user = for_user
        return super().save()

