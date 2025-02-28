from billiard.exceptions import TimeLimitExceeded
from celery.utils.log import get_task_logger
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.db import transaction



logger = get_task_logger(__name__)

@shared_task
def test_code(submission_id):
    """
    Test the code submission with the given ID. Modifies the submission object saving the test results.
    :param submission_id: id of the submission to test
    :return: test results
    """
    logger.info(f"\n ========= Processing submission {submission_id} ========= \n")

    from .service import CodeTestingService
    from submissions.models import CodeSubmission

    service = None

    try:
        with transaction.atomic():
            submission = CodeSubmission.objects.get(pk=submission_id)
            code = submission.code

            service = CodeTestingService(submission_id)

            try:

                results = service.run_tests(submission_code=code)

                with transaction.atomic():

                    submission.result = results['output']
                    submission.save()
                    return results['output']

            except SoftTimeLimitExceeded:
                # raised 5 sec before the hard time limit (10 sec)
                logger.warning(f"Task for submission {submission_id} is approaching timeout limit")

                with transaction.atomic():
                    timeout_message = "Time out. Tu codigo tarda demasiado en ejecutarse. Revisa si no hay ciclos infinitos."
                    submission.result = timeout_message

                    submission.save()
                    return timeout_message

            except ImportError as e:
                logger.error(f"Error running tests: {e}")
                submission.result = f"Error al importar. Asegurate que tu funcion tenga el nombre correcto."
                submission.save()
                return f"Test execution error: {str(e)}"

            except Exception as e:
                logger.exception(f"Error running tests: {e}")
                submission.result = f"Test execution error: {str(e)}"
                submission.save()
                return f"Test execution error: {str(e)}"

    except CodeSubmission.DoesNotExist:
        logger.error(f"Submission {submission_id} not found")
        return "Submission not found"
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return f"Error: {str(e)}"
    finally:
        if 'service' in locals():
            del service
