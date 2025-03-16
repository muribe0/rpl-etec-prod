from django.http import JsonResponse
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

def teacher_required(view_function):
    """
    Decorator for views that checks that the authenticated user is a teacher (has the 'teacher' group).
    Redirects to course list page if the user is not a teacher with a message.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.profile.is_teacher:
            messages.error(request, 'Error. Debes ser docente para ingresar a esta página.')
            return redirect('exercises:course_list')
        return view_function(request, *args, **kwargs)
    return wrapper

def api_login_required(view_function):
    """
    Decorator for views that checks that the user is authenticated.
    If the user is not authenticated, returns a JsonResponse with an error message.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "error": "User not authenticated"
            }, status=403)
        return view_function(request, *args, **kwargs)
    return wrapper