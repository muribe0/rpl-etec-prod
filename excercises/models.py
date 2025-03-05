from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

DEFAULT_INITIAL_CODE = "def funcion():\n    return"

class File(models.Model):
    name = models.CharField()
    content = models.TextField()

class Course(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='courses')

class Unit(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, none=True)

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='units')

class Excercise(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    statement = models.TextField(default="Consigna en el código")
    function_name = models.CharField(max_length=30)
    initial_code = models.TextField(defaul=DEFAULT_INITIAL_CODE)
    test = models.TextField()
    solution = models.TextField(blank=True, none=True)
    # libraries = models.Choices()

    files = models.ManyToManyField(File,
                                   on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             related_name="excercises")
