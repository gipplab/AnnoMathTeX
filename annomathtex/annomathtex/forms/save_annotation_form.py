from django import forms
from ..models.annotation import AnnotationForm


class SaveAnnotationForm(forms.ModelForm):
    """
    This form is used to post an annotation that the user made (e.g. assigning the recommended wikidata item
    energy (Q11379) to the identifier 'E'. The form can then be used to write this information to storage (json file
    or database).
    """
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


