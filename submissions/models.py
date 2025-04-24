from django.db import models
from exercises.models import Exercise
from account.models import Profile

# Create your models here.
class CodeSubmission(models.Model):
    profile = models.ForeignKey(Profile,
                            on_delete=models.CASCADE,
                            related_name="submissions",
                            )
    created_at = models.DateTimeField(auto_now_add=True)

    exercise = models.ForeignKey(Exercise,
                                  on_delete=models.CASCADE,
                                  related_name="submissions",
                                  )
    succes = models.BooleanField(null=True, blank=True)
    code = models.TextField(max_length=100000, default="")
    result = models.TextField(default="Codigo fallido o aun no testeado")


    objects = models.Manager()
