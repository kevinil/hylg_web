from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.CaseData)
admin.site.register(models.User)
admin.site.register(models.Customer)
admin.site.register(models.Clues)
admin.site.register(models.NoCert)