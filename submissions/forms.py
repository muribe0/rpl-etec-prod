from django import forms
from django.forms import Textarea

from .models import CodeSubmission

class CodeSubmissionForm(forms.ModelForm):

    class Meta:
        model = CodeSubmission
        fields = ["code"]

        widgets = {
            "code": Textarea(
                attrs={
                    "cols": 40,
                    "rows": 8,
                    "class": "prism-live line-numbers language-python fill prim-live-source"
                })
        }

        error_messages = {
            "name": {
                "max_length": "Has alcanzado el límite de caracteres."
            }
        }

