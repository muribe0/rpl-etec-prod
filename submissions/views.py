import json
from random import randint

from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from exercises.models import Exercise
from .forms import CodeSubmissionForm
from .models import CodeSubmission

from .tasks import test_code

from .service import test_code_sync



@require_POST
@csrf_exempt
def submit_api(request):
    """
    API endpoint to submit code for testing.
    :param request: POST request with JSON data in its body. The JSON data must contain a 'code' key with the code to test.
    :return: JSON response with the submission_id and task_id of the task that was created to test the code.
    """
    # TODO: check authenticity of request (correct user, exercise, etc)
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
                                                   code=code)
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

