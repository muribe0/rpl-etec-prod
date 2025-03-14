from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'user__first_name', 'dni']
    raw_id_fields = ['user']