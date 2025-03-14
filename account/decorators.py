from django.shortcuts import redirect
from django.contrib import messages

def anonymous_required(view_function):
    """
    Decorator for views that checks that the user is not authenticated, redirecting
    to the course list page if authenticated.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'Error. Ya has iniciado sesión.')
            return redirect('exercises:course_list')
        return view_function(request, *args, **kwargs)
    return wrapper