from django.contrib import admin
from bubble import models


class BaseAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Category, BaseAdmin)
admin.site.register(models.Profile, BaseAdmin)
admin.site.register(models.Document, BaseAdmin)
admin.site.register(models.File, BaseAdmin)
admin.site.register(models.Observation, BaseAdmin)
