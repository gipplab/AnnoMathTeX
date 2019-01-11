from django.forms import ModelForm
from ..models.annotation import AnnotationForm


class SaveAnnotationForm(ModelForm):
    class Meta:
        model = AnnotationForm
        fields = ['user', 'content', 'start_pos', 'end_pos', 'annotation_type']


