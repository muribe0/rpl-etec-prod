from django import forms
from django.contrib.auth.models import User, Group

from exercises.models import Course
from .models import Profile

class ProfileAndUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repetir contraseña',
        widget=forms.PasswordInput
    )
    code = forms.CharField( label='Código de curso',
                            widget=forms.TextInput(attrs={'placeholder': 'El docente debe darles uno.'}),
                            required=False )
    date_of_birth = forms.DateField(
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    dni = forms.CharField(
        label='DNI',
        widget=forms.TextInput(attrs={'placeholder': 'Sin puntos ni espacios (solo números).'}),
        max_length=9,
        required=True
    )


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_code(self):
        cd = self.cleaned_data
        code = cd['code']
        if code:
            for c in code.split('-') :
                if not (c or type(c) == type(str())):
                    raise forms.ValidationError('El código no es válido')
                if not Course.objects.filter(code=c).exists():
                    raise forms.ValidationError('El código no es válido')

        return code

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado')
        domain = email.split('@')[1]
        if domain != 'etec.uba.ar':
            raise forms.ValidationError('El email debe ser de la ETEC (terminar con @etec.uba.ar)')
        return email

    def create_user(self):
        self.full_clean()
        cd = self.clean()

        user = User.objects.create(
            username=cd['email'].split('@')[0],
            email=cd['email'],
            first_name=cd['first_name'],
            last_name=cd['last_name'],
            password=cd['password']
        )

        code = cd['code']
        self.assign_group_and_courses(user, code)

        return user

    def create_profile(self, user):
        cd = self.cleaned_data
        profile = Profile.objects.create(
            user=user,
            dni=cd['dni'],
            date_of_birth=cd['date_of_birth'],
        )
        return profile

    def assign_group_and_courses(self, user, code):
        code_list = code.split('-')

        is_teacher = code and any(map(lambda x: x.first() == 'PROFE', code_list))
        if is_teacher:
            code_list = list(map(lambda x: x[5:] if x[:5] == 'PROFE' else x, code_list))
            group_name = 'teacher'
        else:
            group_name = 'student'

        # assign user to group
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        # create profile and assign courses
        courses = Course.objects.filter(code__in=code_list)

        profile = self.create_profile(user)
        for course in courses:
            profile.courses.add(course)


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.filter(email=data).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Este email ya está registrado')
        if not data.endswith('@etec.uba.ar'):
            raise forms.ValidationError('El email debe ser de la ETEC (terminar con @etec.uba.ar)')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth']

