import json

from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from excercises.models import Excercise
from .forms import CodeSubmissionForm
from .models import CodeSubmission

from .tasks import test_code



@require_POST
@csrf_exempt
def submit_api(request):
    """
    API endpoint to submit code for testing.
    :param request: POST request with JSON data in its body. The JSON data must contain a 'code' key with the code to test.
    :return: JSON response with the submission_id and task_id of the task that was created to test the code.
    """
    # TODO: check authenticity of request (correct user, excercise, etc)
    try:
        data = json.loads(request.body)
        code = data.get('code', "")
        excercise_pk = data.get('excercise_pk', None)

        if not excercise_pk:
            return JsonResponse({
                "error": "Excercise pk not provided"
            }, status=400)

        try:
            with transaction.atomic():
                excercise = Excercise.objects.get(pk=excercise_pk)
                submission = CodeSubmission.objects.create(excercise=excercise,
                                                   code=code)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=500)

        # async task
        res = test_code.delay(submission.pk).id
        print(res)
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

    result = task_result.get()

    return JsonResponse({
        "results": result
    }, status=200)

