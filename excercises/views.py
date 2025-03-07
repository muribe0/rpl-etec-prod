from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ExcerciseForm, UnitForm
from .models import File, Course, Unit, Excercise
from submissions.models import CodeSubmission
from submissions.forms import CodeSubmissionForm

def is_teacher(user):
    return user.is_authenticated() and 'teacher' in user.groups

# Create your views here.

# @login_required(login_url='account:login')
def course_list(request):
    # user = request.user

    # courses = user.created.all() if is_teacher(user) else user.subscribed.all()
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request,
                  'excercises/common/course_list.html',
                  context)


# @login_required(login_url='account:login')
def course_details(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    units = course.units.all()
    context = {
        'units': units,
        'course': course,
    }

    return render(request,
                  'excercises/common/course_details.html',
                  context)


def unit_create(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    form = UnitForm()
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            unit = form.instance
            unit.course = course
            unit.save()
            return redirect('excercises:course_details', course_slug)

    return render(request,
                  'excercises/teachers/unit_create.html',
                  {'form': form,
                   'course': course})

def unit_edit(request, course_slug, unit_pk):
    unit = Unit.objects.get(pk=unit_pk)
    form = UnitForm(instance=unit)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect(unit.course.get_absolute_url())

    return render(request,
                  'excercises/teachers/unit_edit.html',
                  {'form': form,
                   'unit': unit},
                  )

def excercise_details(request, course_slug, excercise_pk):

    excercise = Excercise.objects.get(pk=excercise_pk)

    if excercise.unit.course != Course.objects.get(slug=course_slug):
        return redirect(excercise.unit.course.get_absolute_url())

    form = CodeSubmissionForm()
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)

    context = {
        'excercise': excercise,
        'form': form,
    }

    return render(request,
                  'excercises/common/excercise_details.html',
                  context)


def excercise_create(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    form = ExcerciseForm()
    if request.method == 'POST':
        form = ExcerciseForm(request.POST)
        if form.is_valid():
            form.save()
            excercise = form.instance
            excercise.course = course
            excercise.save()
            return redirect('excercises:course_details', course_slug)

    return render(request,
                    'excercises/teachers/excercise_create.html',
                    {'form': form,
                            'course': course
                     })


def excercise_edit(request, course_slug, excercise_pk):

    excercise = Excercise.objects.get(pk=excercise_pk)

    form = ExcerciseForm(instance=excercise)
    if request.method == 'POST':
        form = ExcerciseForm(request.POST, instance=excercise)
        if form.is_valid():
            form.save()
            return redirect(excercise.get_absolute_url())

    return render(request,
                  'excercises/teachers/excercise_edit.html',
                  {'form': form})