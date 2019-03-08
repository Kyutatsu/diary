from django import forms

from drawing.models import DrawingModel


class DrawingModelForm(forms.ModelForm):
    class Meta:
        model = DrawingModel
        fields = ['title', 'drawing_base64']
