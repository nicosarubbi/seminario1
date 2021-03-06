import datetime
from django import forms
from django.contrib.auth.models import User

from utils.fields import DateField
from bubble import models


class FilterForm(forms.Form):
    profile = forms.ModelChoiceField(label="De", queryset=models.Profile.objects.all(), required=False)
    q = forms.CharField(label="Buscar", required=False)
    

class GroupForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", required=True, max_length=60)
    last_name = forms.CharField(label="Apellido", required=True, max_length=60)
    birthdate = DateField(label='Fecha de Nacimiento', initial=datetime.date.today, required=False)
    relationship = forms.CharField(label="Relación", required=False, max_length=20)

    class Meta:
        model = models.Profile
        fields = ['first_name', 'last_name','birthdate', 'relationship']

class DocumentForm(forms.Form):
    profile = forms.ModelChoiceField(label="Para", queryset=models.Profile.objects.all(), required=True)
    name = forms.CharField(label="Nombre del estudio", required=False)
    date = DateField(label='Fecha', initial=datetime.date.today, required=False)
    category = forms.ModelChoiceField(label="Tipo de Estudio", queryset=models.Category.objects.all(), required=False)
    entity = forms.CharField(label="Laboratorio", required=False)
    professional = forms.CharField(label="Profesional", required=False)
    description = forms.CharField(label="Descripción", max_length=1000, required=False, strip=True, widget=forms.Textarea(attrs={"rows":3}))

    def clean(self):
        data = super().clean()
        if not data.get('name'):
            self.add_error('name', 'Este campo es requerido')
        return data

class VaccineForm(forms.Form):
    profile = forms.ModelChoiceField(label="Para", queryset=models.Profile.objects.all(), required=True)
    name = forms.CharField(label="Nombre de la vacuna", required=False)
    date = DateField(label='Fecha', initial=datetime.date.today, required=False)
    entity = forms.CharField(label="Establecimiento", required=False)
    description = forms.CharField(label="Observaciones", max_length=1000, required=False, strip=True, widget=forms.Textarea(attrs={"rows":3}))

    def clean(self):
        data = super().clean()
        if not data.get('name'):
            self.add_error('name', 'Este campo es requerido')
        return data

class FileForm(forms.Form):
    file = forms.FileField()


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="Nombre", required=True)
    last_name = forms.CharField(label="Apellido", required=True)
    nickname = forms.CharField(label="Apodo", required=False)
    phone = forms.CharField(label="Telefono", required=False)
    birthdate = DateField(label="Fecha de Nacimiento", required=False)
    password = forms.CharField(label="Contraseña", required=False, widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = models.Profile
        fields = ['email', 'first_name', 'last_name', 'nickname', 'phone', 'birthdate', 'password']
        
    def clean(self):
        data = super().clean()
        qs = User.objects.filter(username=data.get('email'))
        if self.instance and self.instance.pk:
            qs = qs.exclude(id=self.instance.user_id)
            if not data.get('password', None):
                # TOOD: validate password
                data.pop('password', None)
        else:
            if not data.get('password', None):
                self.add_error('email', 'Este campo es requerido')
        if qs.exists():
            self.add_error('email', 'Ya existe un usuario con este email')
        return data