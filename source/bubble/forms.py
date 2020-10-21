import datetime
from django import forms
from bubble import models
from utils.fields import DateField
from django.core.exceptions import ValidationError

class DocumentForm(forms.Form):
    name = forms.CharField(label="Nombre del estudio", required=False)
    date = DateField(label='Fecha', initial=datetime.date.today, required=False)
    category = forms.ModelChoiceField(label="Tipo de Estudio", queryset=models.Category.objects.all(), required=False)
    entity = forms.CharField(label="Laboratorio", required=False)
    professional = forms.CharField(label="Profesional", required=False)

    def clean(self):
        data = super().clean()
        if not data.get('name'):
            self.add_error('name', 'Este campo es requerido')
        if not data.get('category'):
            self.add_error('category', 'Este campo es requerido')
        return data

class FileForm(forms.Form):
    file = forms.FileField()
