from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import File, Course, Unit, Excercise


def is_teacher(user):
    return user.is_authenticated() and 'teacher' in user.groups

# Create your views here.

# @login_required(login_url='account:login')
def course_list(request):
    user = request.user

    courses = user.created.all() if is_teacher(user) else user.subscribed.all()

    context = {
        'courses': courses,
    }
    return render(request,
                  'excercises/common/templates/excercises/common/course_list.html',
                  context)


# @login_required(login_url='account:login')
def unit_list(request, course_slug, pk):
    course = Course.object.get(slug=course_slug, pk=pk)
    units = course.units
    context = {
        'units': units,
    }

    return render(request,
                  'excercises/common/templates/excercises/common/unit_list.html',
                  context)

