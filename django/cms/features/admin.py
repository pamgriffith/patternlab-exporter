from django.contrib import admin

# Register your models here.
from .models import Feature

class FeatureAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("title",)}

admin.site.register(Feature)