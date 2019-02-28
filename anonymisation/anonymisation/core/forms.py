from django import forms

from anonymisation.core.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', )
