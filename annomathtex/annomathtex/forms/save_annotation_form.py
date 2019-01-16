from django import forms
from ..models.annotation import AnnotationForm


class SaveAnnotationForm(forms.ModelForm):
    class Meta:
        model = AnnotationForm
        #fields = ['user', 'content', 'start_pos', 'end_pos', 'annotation_type']
        fields = ['text']
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'id': 'post-text',
                    'required':True,
                    'placeholder': 'annotation placeholder....'
                }),
        }


