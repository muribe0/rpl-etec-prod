from django.db import models
# from excercises.models import Excercise

# Create your models here.
class CodeSubmission(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    # excercises = models.ForeignKey(Excercise,
    #                                on_delete=models.CASCADE,
    #                                related_name="submissions")
    succes = models.BooleanField(null=True, blank=True)
    code = models.TextField(max_length=100000, default="")
    result = models.TextField(default="Codigo fallido o aun no testeado")


    objects = models.Manager()
# docker compose exec web python /code/manage.py migrate
