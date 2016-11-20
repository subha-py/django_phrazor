from django import forms

from files.models import File

class FileForm(forms.ModelForm):
    file=forms.FileField(label='Upload File')
    class Meta:
        model=File
        fields=['name','desc']

    field_order = ('name','desc','file')

    def clean_file(self):
        file=self.cleaned_data.get('file')
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('Only csv files are supported now')

        return file

    def save(self, for_user):
        self.instance.user = for_user
        return super().save()

