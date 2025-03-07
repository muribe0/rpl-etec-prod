from django.shortcuts import render, redirect

from .forms import ExerciseForm, UnitForm
from .models import File, Course, Unit, Exercise
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
                  'exercises/common/course_list.html',
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
                  'exercises/common/course_details.html',
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
            return redirect('exercises:course_details', course_slug)

    return render(request,
                  'exercises/teachers/unit_create.html',
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
                  'exercises/teachers/unit_edit.html',
                  {'form': form,
                   'unit': unit},
                  )

def exercise_details(request, course_slug, exercise_pk):

    exercise = Exercise.objects.get(pk=exercise_pk)

    if exercise.unit.course != Course.objects.get(slug=course_slug):
        return redirect(exercise.unit.course.get_absolute_url())

    form = CodeSubmissionForm()
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)

    context = {
        'exercise': exercise,
        'form': form,
    }

    return render(request,
                  'exercises/common/exercise_details.html',
                  context)


def exercise_create(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    form = ExerciseForm()
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            exercise = form.instance
            exercise.course = course
            exercise.save()
            return redirect('exercises:course_details', course_slug)

    return render(request,
                  'exercises/teachers/exercise_create.html',
                  {'form': form,
                   'course': course
                   })


def exercise_edit(request, course_slug, exercise_pk):

    exercise = Exercise.objects.get(pk=exercise_pk)

    form = ExerciseForm(instance=exercise)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect(exercise.get_absolute_url())

    return render(request,
                  'exercises/teachers/exercise_edit.html',
                  {'form': form})
