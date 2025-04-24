from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'dni', 'is_student', 'is_teacher']
    list_filter = ['user__groups', 'courses']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'dni']
    filter_horizontal = ['courses']

    def is_student(self, obj):
        return obj.is_student
    is_student.boolean = True

    def is_teacher(self, obj):
        return obj.is_teacher
    is_teacher.boolean = True