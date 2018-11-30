from django import forms


class FilePathForm(forms.Form):
    #path = forms.CharField(label='Path', max_length=250)
    path = forms.FileField(label='File')
