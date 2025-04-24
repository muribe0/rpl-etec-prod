from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.decorators import teacher_required
from .forms import ExerciseForm, UnitForm
from .models import File, Course, Unit, Exercise
from submissions.forms import CodeSubmissionForm

from account.decorators import teacher_required, profile_required


@login_required
@profile_required
def course_list(request):
    user = request.user

    courses = user.profile.courses.all()
    context = {
        'courses': courses,
    }
    return render(request,
                  'exercises/common/course_list.html',
                  context)


@login_required
def course_details(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    if course not in request.user.profile.courses.all():
        messages.error(request, 'Error. No tienes acceso a este curso.') # TODO migrate to decorator
        return redirect('exercises:course_list')
    units = course.units.all()
    context = {
        'units': units,
        'course': course,
    }

    return render(request,
                  'exercises/common/course_details.html',
                  context)

@login_required
@teacher_required
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

@login_required
@teacher_required
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

@login_required
@profile_required
def exercise_details(request, course_slug, exercise_pk):

    exercise = Exercise.objects.get(pk=exercise_pk)

    if exercise.unit.course != Course.objects.get(slug=course_slug):
        return redirect(exercise.unit.course.get_absolute_url())

    form = CodeSubmissionForm()
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)

    previous_submissions = exercise.submissions.filter(profile=request.user.profile).order_by('-created_at')


    context = {
        'exercise': exercise,
        'form': form,
        'previous_submissions': previous_submissions,
    }

    return render(request,
                  'exercises/common/exercise_details.html',
                  context)


@login_required
@teacher_required
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

@login_required
@teacher_required
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
                  {'form': form,
                           'exercise': exercise})
