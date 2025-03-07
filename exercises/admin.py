from django.contrib import admin
from .models import Course, Unit, Exercise, File

# Register your models here.

# @admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)
    ordering = ('pk',)



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    search_fields = ('title', 'slug')
    ordering = ('pk',)
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'course__title')
    search_fields = ('title', 'slug')
    ordering = ('pk',)
    prepopulated_fields = {'slug': ('title',)}


# @admin.register(Exercise)
# class ExerciseAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'title', 'unit__title')
#     search_fields = ('title', 'slug')
#     ordering = ('pk',)
#     prepopulated_fields = {'slug': ('title',)}
