import celery
from celery.utils.log import get_task_logger
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.db import transaction

from rpl.settings import CELERY_TASK_SOFT_TIME_LIMIT, CELERY_TASK_TIME_LIMIT

logger = get_task_logger(__name__)



@shared_task(soft_time_limit=CELERY_TASK_SOFT_TIME_LIMIT, time_limit=CELERY_TASK_TIME_LIMIT)
def test_code(submission_id):
    """
    Test the code submission with the given ID. Modifies the submission object saving the test results.
    :param submission_id: id of the submission to test
    :return: test results
    """

    from submissions.service import CodeTestingService
    from submissions.models import CodeSubmission

    service = CodeTestingService(submission_id)
    results = service.run_tests()
    submission = CodeSubmission.objects.get(pk=submission_id)
    submission.result = results['output']
    submission.save()
    return results['output']

    # logger.info(f"\n ========= Processing submission {submission_id} ========= \n")
    #
    # from submissions.service import CodeTestingService
    # from submissions.models import CodeSubmission
    #
    # service = None
    #
    # try:
    #     with transaction.atomic():
    #         submission = CodeSubmission.objects.get(pk=submission_id)
    #         code = submission.code
    #         try:
    #             service = CodeTestingService(submission_id)
    #             results = service.run_tests()
    #
    #             with transaction.atomic():
    #                 submission.result = results['output']
    #                 submission.save()
    #                 print('results:', results['output'])
    #                 return results['output']
    #
    #         except SoftTimeLimitExceeded:
    #             logger.warning(f"Task for submission {submission_id} is approaching timeout limit")
    #
    #             with transaction.atomic():
    #                 timeout_message = "Time out. Tu codigo tarda demasiado en ejecutarse. Revisa si no hay ciclos infinitos."
    #                 submission.result = timeout_message
    #                 submission.save()
    #                 return timeout_message
    #
    #         except Exception as e:
    #             logger.exception(f"Error running tests: {e}")
    #             submission.result = f"Test execution error: {str(e)}"
    #             submission.save()
    #             return f"Test execution error: {str(e)}"
    #
    # except CodeSubmission.DoesNotExist:
    #     logger.error(f"Submission {submission_id} not found")
    #     return "Submission not found"
    # except Exception as e:
    #     if submission:
    #         with transaction.atomic():
    #             submission.result = f"Error: {str(e)}"
    #             submission.save()
    #     return f"Error: {str(e)}"
    # finally:
    #     if 'service' in locals():
    #         del service
