from django.db import models


class AnnotationForm(models.Model):
    """
    The annotations that a user makes are stored as AnnotationForm objects.
    """
    text = models.CharField(max_length=20)
    user = models.CharField(max_length=20)
    content = models.CharField(max_length=20)
    start_pos = models.IntegerField()
    end_pos = models.IntegerField()
    annotation_type = models.CharField(max_length=20)


    """def clean_data(self):
        clean = super(AnnotationForm, self).clean()
        user = clean.get('user')
        content = clean.get('content')
        start_pos = clean.get('start_pos')
        end_pos = clean.get('end_pos')
        annotation_type = clean.get('annotation_type')"""



