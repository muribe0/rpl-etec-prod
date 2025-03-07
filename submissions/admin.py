from django.contrib import admin
from .models import CodeSubmission

# Register your models here.

@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'code', 'result', 'exercise__title')
    list_filter = ('created_at',)
    search_fields = ('code', 'result')
    ordering = ('-created_at',)
