from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import ProfileAndUserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .decorators import anonymous_required

from .mail_service import send_confirmation_email
# Create your views here.


@anonymous_required
def register(request):
    if request.method != 'POST':
        form = ProfileAndUserRegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    form = ProfileAndUserRegistrationForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'account/register.html', {'form': form})

    new_user = form.create_user()
    new_user.is_active = False # Inactive users cannot log in as expected.
    new_user.save()

    try:
        sent = send_confirmation_email(new_user)
    except Exception as e:
        new_user.delete()

        messages.error(request, f'Error al enviar correo de confirmación. (Error: {str(e)})')
        return render(request, 'account/register.html', {'form': form})

    return render(request, 'account/register_done.html', {'new_user': new_user})


@anonymous_required
def register_confirm(request, user_pk, token):
    """
    Confirms the registration of a user by comparing the token with the hash of the username.
    If the token is valid, the user is activated. Otherwise, an error message is shown and the user is redirected to
    the registration page.
    :param user_pk: The user's primary key
    :param token: The token
    """
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('account:register')

    valid_token = int(hash(user.username))
    valid_token = valid_token if valid_token > 0 else -valid_token
    if valid_token != token:
        messages.error(request, 'Token no válido')
        return redirect('account:register')

    user.is_active = True
    user.save()

    messages.success(request, 'Cuenta confirmada')

    return render(request, 'account/register_confirm.html', {'validlink':True})

@login_required
def edit(request):
    if request.method != 'POST':
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    else:
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Perfil actualizado')
        else:
            messages.error(request, 'Error al actualizar perfil')

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    render(request,
           'account/edit.html',
           context)