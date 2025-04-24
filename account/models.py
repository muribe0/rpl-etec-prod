from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from exercises.models import Course
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    date_of_birth = models.DateField(blank=True, null=True)
    dni = models.CharField(max_length=8, unique=True)
    courses = models.ManyToManyField(Course, related_name='profiles', blank=True)

    @property #this makes it a getter
    def is_student(self):
        return self.user.groups.filter(name='student').exists()

    @property
    def is_teacher(self):
        return self.user.groups.filter(name='teacher').exists()

    @property
    def get_courses(self):
        return self.courses.all()

    # a CodeSubmission has a FK to Profile, no matter if it's a student or a teacher since both can submit code

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return f'Profile for user {self.user.username}'


    # The idea is to TODO create a profile and if the user puts a CODE in the registration form,
    # and it corresponds to an existing course, then the user is added to that course
    # if the user is a student -> he is added to the course
    # if the user is a teacher -> he is added as the creator of the course
    # this differentiation is made by the is_student and is_teacher properties only
