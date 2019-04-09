from django import forms


class UploadFileForm(forms.Form):
    """
    A very simple form that is allows the user to select a file that he wants to load into memory and annotate.
    """

    #title = forms.CharField(max_length=50)
    file = forms.FileField(label='File')
