from django.shortcuts import render
from .forms import UserRegistrationForm
# Create your views here.

def register(request):
    if request.method != 'POST':
        form = UserRegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    form = UserRegistrationForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'account/register.html', {'form': form})

    new_user = form.save(commit=False)
    new_user.set_password(form.cleaned_data['password'])
    new_user.save()
    return render(request, 'account/register_done.html', {'new_user': new_user})
