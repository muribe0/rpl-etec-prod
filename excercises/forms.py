from .models import File, Course, Unit, Excercise
from django import forms

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = '__all__'

        labels = {
            'name': 'nombre completo del archivo'
            ''
        }

    def clean_name(self):
        data = self.cleaned_data['name']
        extensions = {'.txt', '.csv', '.py'}
        for ext in extensions:
            if ext in data:
                return data
        allowed = ' - '.join(extensions)
        raise forms.ValidationError(f"El archivo no tiene una extensión adecuada ({allowed}).")


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'title', 'description'
        ]

        labels = {
            'title' : 'título',
            'description': 'descripción'
        }


class ExcerciseForm(forms.ModelForm):
    class Meta:
        model = Excercise
        fields = [
            'title',
            'statement',
            'function_name',
            'initial_code',
            'test',
            'unit'
        ]

        labels = {
            'title' : 'título',
            'statement' : 'consigna',
            'function_name' : 'nombre de la función',
            'initial_code' : 'código inicial',
            'unit' : 'unidad'
        }

    def clean_initial_code(self):
        cd = self.cleaned_data
        if cd['function_name'] not in cd['initial_code']:

            raise forms.ValidationError("El nombre de la función no se encuentra en el código inicial")
        return cd['function_name']

