from django.shortcuts import render
from .forms import ProfileAndUserRegistrationForm
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
