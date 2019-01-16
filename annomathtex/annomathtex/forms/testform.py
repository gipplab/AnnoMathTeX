from django import forms


class TestForm(forms.Form):
    test = forms.CharField(max_length=50)
