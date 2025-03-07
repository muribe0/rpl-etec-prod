from django.db.models import manager
from django.db import models
from django.contrib.auth.models import Group
from django.urls.base import reverse
from django.utils.text import slugify

# Create your models here.

DEFAULT_INITIAL_CODE = "def funcion():\n    return"

class File(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()

class Course(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    groups = models.ManyToManyField(Group,
                              related_name='courses',
                                    blank=True)

    objects = manager.Manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Check if there is another course with the same slug
        is_current = None
        if self.pk:
            is_current = Course.objects.get(pk=self.pk)

        original_slug = self.slug
        counter = 1
        while not is_current and Course.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        print(self.slug)
        super().save(*args, *kwargs)

    def get_url(self, view):
        return reverse(
            f'excercises:{view}',
            args=[self.slug]
        )

    def get_absolute_url(self):
        return self.get_url('course_details')

    def get_excercise_create_url(self):
        return self.get_url('excercise_create')

    def get_unit_create_url(self):
        return self.get_url('unit_create')


class Unit(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='units',
                               blank=True)

    objects = manager.Manager()

    def get_url(self, view):
        return reverse(

            f'excercises:{view}',
            args=[self.course.slug, self.pk]
        )

    def get_edit_url(self):
        return self.get_url('unit_edit')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save( *args, *kwargs)


class Excercise(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    statement = models.TextField(default="Consigna en el código")
    function_name = models.CharField(max_length=30)
    initial_code = models.TextField(default=DEFAULT_INITIAL_CODE)
    dificulty = models.PositiveSmallIntegerField(default=1)
    test = models.TextField()
    solution = models.TextField(blank=True, null=True)

    # libraries = models.Choices()
    # files = models.ManyToManyField(File, blank=True, null=True)
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             related_name="excercises")

    objects = manager.Manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.initial_code == DEFAULT_INITIAL_CODE:
            self.initial_code = self.initial_code.replace('funcion', self.function_name)

        super().save(*args, *kwargs)

    def clean_inital_code(self):
        if self.function_name not in self.initial_code:
            return False # TODO change this
        return self.initial_code

    def get_url(self, view):
        return reverse(
            f'excercises:{view}',
            args=[self.unit.course.slug , self.pk]
        )

    def get_absolute_url(self):
        return self.get_url('excercise_details')

    def get_edit_url(self):
        return self.get_url('excercise_edit')

    def get_complete_test_code(self, solution_file_path):
        return f"from {solution_file_path} import {self.function_name} as foo\n{self.test}"