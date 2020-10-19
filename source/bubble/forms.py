import datetime
from django import forms
from bubble import models
from utils.fields import DateField
from django.core.exceptions import ValidationError

class DocumentForm(forms.Form):
    name = forms.CharField(label="Nombre del estudio")
    date = DateField(label='Fecha', initial=datetime.date.today)
    category = forms.ModelChoiceField(label="Tipo de Estudio", queryset=models.Category.objects.all())
    entity = forms.CharField(label="Laboratorio", required=False)
    professional = forms.CharField(label="Profesional", required=False)

    def clean(self):
        data = super().clean()
        date = data.get('date')
        if date > datetime.date.today():
            self.add_error('date', 'Fecha inválida.')
            raise ValidationError('Ups... algún campo está mal')
        return data
