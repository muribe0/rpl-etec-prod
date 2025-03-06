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
    slug = models.SlugField(max_length=100)
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='courses')

    object = manager.Manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(self, *args, *kwargs)

    def get_url(self, view):
        return reverse(
            f'studygroups:{view}',
            args=[self.slug]
        )

    def get_absolute_url(self):
        return self.get_url('course_details')


class Unit(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='units')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(self, *args, *kwargs)


class Excercise(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    statement = models.TextField(default="Consigna en el código")
    function_name = models.CharField(max_length=30)
    initial_code = models.TextField(default=DEFAULT_INITIAL_CODE)
    difiiculty = models.PositiveSmallIntegerField(default=1)
    test = models.TextField()
    solution = models.TextField(blank=True, null=True)

    # libraries = models.Choices()
    # files = models.ManyToManyField(File, blank=True, null=True)
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             related_name="excercises")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.initial_code == DEFAULT_INITIAL_CODE:
            self.initial_code = self.initial_code.replace('funcion', self.function_name)

        super().save(self, *args, *kwargs)

    def clean_inital_code(self):
        if self.function_name not in self.initial_code:
            return False # TODO change this
        return self.initial_code
