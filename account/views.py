from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ProfileAndUserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method != 'POST':
        form = ProfileAndUserRegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    form = ProfileAndUserRegistrationForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'account/register.html', {'form': form})

    new_user = form.create_user()

    return render(request, 'account/register_done.html', {'new_user': new_user})

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