from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Paper
from .models import Category

from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(Paper)
class PaperAdmin(SummernoteModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"url": ("title",)}
    summernote_fields = ('content',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"url": ("name",)}