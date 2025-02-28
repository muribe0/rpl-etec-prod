import json
import uuid

from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from submissions.forms import CodeSubmissionForm
from submissions.models import CodeSubmission

from .tasks import test_code


def index(request):
    if request.method == "GET":
        return render(request,
                      "submissions/index.html",
                      {"form": CodeSubmissionForm()})

    form = CodeSubmissionForm(request.POST)
    if not form.is_valid():
        return render(request,
                      "submissions/index.html",
                      {"form": form})

    context = {
        'form': form,
    }
    return render(request, "submissions/index.html", context)


@require_POST
@csrf_exempt
def submit_api(request):
    """
    API endpoint to submit code for testing.
    :param request: POST request with JSON data in its body. The JSON data must contain a 'code' key with the code to test.
    :return: JSON response with the submission_id and task_id of the task that was created to test the code.
    """
    try:
        data = json.loads(request.body)
        code = data.get('code', "")

        submission = CodeSubmission.objects.create(code=code)

        unique_id = data.get('unique_id', submission.pk)
        res = test_code.delay(unique_id).id

        return JsonResponse({
            "submission_id": unique_id,
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


def auto_submit(request, num):
    code_0 = """
def suma(x, y):
    return suma(x,y)
    """

    code_1 = """
def suma(x, y):
    c = 0
    for i in range(100000000000000000):
        c += i
    return x + y
    """

    code_2 = """
def suma(x,y): 
    return x + y
    """

    codes = [code_0, code_1, code_2]

    submission = CodeSubmission.objects.create(code=codes[num])

    # async task
    test_code.delay(submission.pk)

    return render(request, "submissions/submit.html", {'form': CodeSubmissionForm()})


def submit(request):
    if request.method == "GET":
        return render(request,
                      "submissions/submit.html",
                      {"form": CodeSubmissionForm()})

    form = CodeSubmissionForm(request.POST)

    if not form.is_valid():
        return render(request,
                      "submissions/submit.html",
                      {"form": form})

    submission = CodeSubmission.objects.create(code=form.cleaned_data['code'])

    # async task
    test_code.delay(submission.pk)

    return render(request, "submissions/submit.html", {'form': form})
