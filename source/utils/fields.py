# -*- coding: utf-8 -*-

from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.db.models import OneToOneField
from django import forms
from bootstrap_datepicker_plus import DatePickerInput


class DateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = DatePickerInput(format='%Y-%m-%d')
        super().__init__(*args, **kwargs)


class CustomReverseOneToOneDescriptor(ReverseOneToOneDescriptor):
    def __get__(self, instance, cls=None):
        try:
            return super().__get__(instance, cls)
        except self.RelatedObjectDoesNotExist:
            return None


class OneToOneField(OneToOneField):
    related_accessor_class = CustomReverseOneToOneDescriptor
