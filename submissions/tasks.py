import celery
from celery.utils.log import get_task_logger
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.db import transaction

from rpl.settings import CELERY_TASK_SOFT_TIME_LIMIT, CELERY_TASK_TIME_LIMIT

logger = get_task_logger(__name__)


@shared_task(soft_time_limit=CELERY_TASK_SOFT_TIME_LIMIT, time_limit=CELERY_TASK_TIME_LIMIT,
             name='submissions.tasks.test_code')
def test_code(submission_id):
    """
    Test the code submission with the given ID. Modifies the submission object saving the test results.
    :param submission_id: id of the submission to test
    :return: test results
    """
    from submissions.service import CodeTestingService
    from submissions.models import CodeSubmission
    
    # Make sure these are defined somewhere in your module
    MSG_TIMEOUT = "Time out. Tu codigo tarda demasiado en ejecutarse. Revisa si no hay ciclos infinitos."
    MSG_TEST_ERROR = "Test execution error: {}"
    
    logger.info(f"Starting test_code task for submission_id: {submission_id}")
    service = None
    submission = None
    try:
        # Query for the submission first
        submission = CodeSubmission.objects.get(pk=submission_id)
        
        try:
            service = CodeTestingService(submission_id)
            results = service.run_tests()
            
            # Use transaction for saving results
            submission.result = results
            submission.save()
            return results
            
        except SoftTimeLimitExceeded:
            with transaction.atomic():
                submission.result = MSG_TIMEOUT
                submission.save()
            return MSG_TIMEOUT
            
        except Exception as e:
            with transaction.atomic():
                submission.result = MSG_TEST_ERROR.format(str(e))
                submission.save()
            return MSG_TEST_ERROR.format(str(e))
            
    except CodeSubmission.DoesNotExist:
        logger.error(f"Submission {submission_id} not found")
        return "Submission not found"
    except Exception as e:
        if submission:
            with transaction.atomic():
                submission.result = f"Error: {str(e)}"
                submission.save()
        return f"Error: {str(e)}"
    finally:
        if 'service' in locals():
            del service