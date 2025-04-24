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
                    #"class": "code-editor prism-live line-numbers language-python fill prim-live-source",
                    "class": "code-editor",
                    "cols": 40,
                    "rows": 8,
                    "style": "width: 100%; height: 100%; resize: none;",
                    "spellcheck": "false",
                    "autocomplete": "off",
                    "autocorrect": "off",
                    "autocapitalize": "off",
                })
        }

        error_messages = {
            "name": {
                "max_length": "Has alcanzado el límite de caracteres."
            }
        }
