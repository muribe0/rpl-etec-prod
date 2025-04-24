import json
from random import randint

from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from account.decorators import api_login_required
from exercises.models import Exercise
from .forms import CodeSubmissionForm
from .models import CodeSubmission

from .tasks import test_code


@require_POST
@csrf_exempt
@api_login_required
def submit_api(request):
    """
    API endpoint to submit code for testing.
    :param request: POST request with JSON data in its body. The JSON data must contain a 'code' key with the code to test.
    :return: JSON response with the submission_id and task_id of the task that was created to test the code.
    """
    # TODO: check authenticity of request (correct user, exercise, etc)
    try:
        profile = request.user.profile
    except AttributeError:
        return JsonResponse({
            "error": "User not authenticated"
        }, status=403)

    try:
        data = json.loads(request.body)
        code = data.get('code', "")
        exercise_pk = data.get('exercise_pk', None)

        if not exercise_pk:
            return JsonResponse({
                "error": "Exercise pk not provided"
            }, status=400)

        try:
            with transaction.atomic():
                exercise = Exercise.objects.get(pk=exercise_pk)
                submission = CodeSubmission.objects.create(exercise=exercise,
                                                   code=code, profile=request.user.profile)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=500)

        # async task
        res = test_code.delay(submission.pk).id

        return JsonResponse({
            "submission_id": submission.pk,
            "task_id": res
        }, status=200)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON data"
        }, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({
            "error": str(e)
        }, status=500)
    finally:
        pass

@csrf_exempt
@api_login_required
def results_api(request, task_id):
    """
    API endpoint to get the results of a task. The task_id is the id of the task that was returned when the code was submitted.
    :param request: GET request with the task_id as a parameter.
    :param task_id: id of the task to get the results from.
    :return: JSON response with the results of the task.
    """


    task_result = AsyncResult(task_id, app=test_code)

    if task_result.ready() and task_result.failed():
        return JsonResponse({
            "error": "Task failed",
            "results": "Task not found"
        }, status=500)

    result = task_result.get(timeout=5)
    # result = CodeSubmission.objects.filter().last().result

    return JsonResponse({
        "results": str(result)
    }, status=200)


@require_GET
@api_login_required
def previous_submissions_api(request):
    try:
        data = json.loads(request.body)
        exercise_pk = data.get('exercise_pk', None)
        if not exercise_pk:
            return JsonResponse({
                "error": "Exercise pk not provided"
            }, status=400)

        exercise = Exercise.objects.get(pk=exercise_pk)
    except Exercise.DoesNotExist:
        return JsonResponse({
            "error": "Exercise not found"
        }, status=404)

    try:
        user_submissions = request.user.profile.submissions.all().filter(exercise=exercise)
    except CodeSubmission.DoesNotExist:
        return JsonResponse({
            "error": "No submissions found"
        }, status=404)

    submissions = []
    for submission in user_submissions:
        submissions.append({
            "submission_id": submission.pk,
            "code": submission.code,
            "result": submission.result,
            "success": submission.success
        })

    return JsonResponse({
        "submissions": submissions
    }, status=200)
