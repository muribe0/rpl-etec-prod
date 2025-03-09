from django import forms
from django.contrib.auth import get_user_model

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repetir contraseña',
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado')
        domain = email.split('@')[1]
        if domain != 'etec.uba.ar':
            raise forms.ValidationError('El email debe ser de la ETEC (terminar con @etec.uba.ar)')
        return email

