import tempfile
import os
from io import StringIO
from contextlib import contextmanager
import unittest
from celery.exceptions import SoftTimeLimitExceeded

from submissions.models import CodeSubmission


class CodeTestingService:
    def __init__(self, submission_id):
        self.unique_id = submission_id
        self.test_dir = os.path.join(tempfile.gettempdir(), f"test_{self.unique_id}")
        try:
            self.submission = CodeSubmission.objects.get(pk=self.unique_id)
        except CodeSubmission.DoesNotExist:
            raise FileNotFoundError


    def __del__(self):
        self.cleanup_directory(self.test_dir)

    @contextmanager
    def create_test_environment(self):

        # create unique test dir
        os.makedirs(self.test_dir)

        try:
            # create files
            solution_path = os.path.join(self.test_dir, f'solution_{self.unique_id}.py')
            code_test_path = os.path.join(self.test_dir, f'test_solution_{self.unique_id}.py')

            # write files
            with open(solution_path, 'w') as f:
                f.write(self.submission.code)

            with open(code_test_path, 'w') as f:
                try:
                    exercise = self.submission.exercise
                except:
                    raise ValueError("Submission does not have an exercise")

                f.write(exercise.get_complete_test_code(f'solution_{self.unique_id}.py'))

            yield self.test_dir

        finally:  # once test_dir has been used, we delete everything
            self.cleanup_directory(self.test_dir)

    # define a timeout wrapper
    @staticmethod
    def timeout_wrapper(timeout_seconds=4):
        from functools import wraps
        import threading
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = [None]

                def target():
                    result[0] = func(*args, **kwargs)

                # create thread to run target (runner.run) function
                thread = threading.Thread(target=target)
                # set the thread as a daemon so it is killed when the main thread is killed
                thread.daemon = True
                # start the thread
                thread.start()
                # wait for the thread to finish or timeout
                thread.join(timeout_seconds)

                # if the thread is still alive, it means it has not finished
                if thread.is_alive():
                    # raise this exception to let celery task handle it
                    raise SoftTimeLimitExceeded

                # if the thread has finished, return the result
                return result[0]

            return wrapper

        return decorator

    def run_tests(self):

        with self.create_test_environment() as test_dir:
            loader = unittest.TestLoader()
            suite = loader.discover(test_dir, pattern=f'test_solution_{self.unique_id}.py')
            full_output = StringIO()

            # Create a runner with custom timeout
            runner = unittest.TextTestRunner(stream=full_output, verbosity=2)

            # save the original run method
            original_run = runner.run

            # replace the run method with timeout version
            runner.run = self.timeout_wrapper(4)(original_run)

            # Run the tests with the timeout-enabled run method
            result = runner.run(suite)

            return self.format_results(result, full_output)


    @staticmethod
    def cleanup_directory(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(directory)


    def _get_file_test_code(self):
        with open('submissions/testing/test_suma.py', 'r') as f:
            test_code = f.read()
            return f"from solution_{self.unique_id} import suma as foo\n" + test_code


    @staticmethod
    def format_results(result, full_output):

        failures = []
        for fail, description in result.failures:
            method_name = fail._testMethodName
            short_description = "".join(description.split("\n")[-2:]).strip()
            failures.append(f'{method_name}() ---> "{short_description}"... FAIL')

        errors = []
        for error, description in result.errors:
            method_name = error._testMethodName
            short_description = "".join(description.split("\n")[-3:]).strip()
            errors.append(f'{method_name}() ---> "{short_description}"... ERROR')

        return {
            'tests_run': result.testsRun,
            'failures': failures,
            'errors': errors,
            'success': result.wasSuccessful(),
            'output': full_output.getvalue()
        }




