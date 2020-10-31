from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from bubble import models


class ChangeFormLinkMixin(object):
    def change_form_link(self, instance):
        if instance.id:
            url = reverse(f'admin:{instance._meta.app_label}_{instance._meta.model_name}_change', args=(instance.id,))
            return format_html(f'<a href="{url}">edit</a>')
        url = reverse(f'admin:{instance._meta.app_label}_{instance._meta.model_name}_add')
        return format_html(f'<a href="{url}">add</a>')


def inline(related_model, stacked=False, raw_ids=None, link=False, name=None):
    parent = admin.StackedInline if stacked else admin.TabularInline

    class Inline(parent, ChangeFormLinkMixin):
        model = related_model
        extra = 0
        raw_id_fields = raw_ids or []
        readonly_fields = ['change_form_link'] if link else []
        verbose_name_plural = name or parent.verbose_name_plural

    return Inline


admin.site.register(models.Category)
admin.site.register(models.Profile)
admin.site.register(models.Document)
admin.site.register(models.File)
admin.site.register(models.Calendar)
admin.site.register(models.Vaccine)
