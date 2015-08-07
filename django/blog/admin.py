from django.contrib import admin

# Register your models here.
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("title",)}

admin.site.register(Blog, BlogAdmin)