from django.contrib import admin
from bubble import models


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Profile, ProfileAdmin)
