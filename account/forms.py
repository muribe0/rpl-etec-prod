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
    code = forms.CharField(
        label='Código de curso',
        widget=forms.TextInput(attrs={'placeholder': 'El docente debe darles uno.',
                                      'required': False}),
    )
    date_of_birth = forms.DateField(
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_code(self):
        cd = self.cleaned_data
        code = cd['code']
        if code:
            for c in code.split('-') :
                if not (c or type(c) == type(str()) or len(c) == 6):
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


    def save_student(self, user, courses):
        cd = self.cleaned_data
        student = Profile(
            user=user,
            dni=cd['dni'],
            date_of_birth=cd['date_of_birth'],
        )
        for c in courses:
            student.courses.add(c)

        student.save()

        user.groups.add(Group.objects.get_or_create(name='student')[0])


    def save_teacher(self, user, courses):
        cd = self.cleaned_data
        teacher = Profile(
            user=user,
            dni=cd['dni'],
            date_of_birth=cd['date_of_birth'],
        )
        for c in courses:
            teacher.courses.add(c)

        teacher.save()

        group = Group.objects.get_or_create(name='teacher')[0]
        user.groups.all().add(group)


    def create_user(self):
        self.full_clean()
        cd = self.clean()

        user = User.objects.create(
            username=cd['email'].split('@')[0],
            email=cd['email'],
            first_name=cd['first_name'],
            last_name=cd['last_name'],
            paswword = cd['password']
        )

        code = cd['code']
        if code:
            code_list = code.split('-')
            courses = Course.objects.filter(code__in=code_list)

            # If the code starts with T, the user is a teacher
            if any(map(lambda x: x.first() == 'T', code_list)):
                self.save_teacher(user, courses)
            else:
                self.save_student(user, courses)

        return user
