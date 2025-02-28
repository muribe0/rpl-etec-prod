import tempfile
import os
from io import StringIO
from contextlib import contextmanager
import unittest

from django.contrib.admin.templatetags.admin_list import results


class CodeTestingService:
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.test_dir = os.path.join(tempfile.gettempdir(), f"test_{self.unique_id}")
        print(f"\nDIR:{self.test_dir}\n")
    def __del__(self):
        try:
            self.cleanup_directory(self.test_dir)
        except FileNotFoundError:
            pass

    @contextmanager # converts the function into a context manager to be used with the 'with' statement
    def create_test_environment(self, submission_code):

        # create unique test dir

        os.makedirs(self.test_dir)

        try:
            # create files
            code_path = os.path.join(self.test_dir, f'solution_{self.unique_id}.py')
            code_test_path = os.path.join(self.test_dir, f'test_solution_{self.unique_id}.py')

            # write files
            with open(code_path, 'w') as f:
                f.write(submission_code)

            with open(code_test_path, 'w') as f:
                f.write(self.get_test_code())

            yield self.test_dir

        finally:  # once test_dir has been used, we delete everything
            self.cleanup_directory(self.test_dir)


    def run_tests(self, submission_code):

        with self.create_test_environment(submission_code) as test_dir:
            loader = unittest.TestLoader()
            # a TestSuite is a collection of test cases, test suites, or both.
            # It is used to aggregate tests that should be executed together.
            suite = loader.discover(test_dir, pattern=f'test_solution_{self.unique_id}.py')
            # run tests with a custom result collector
            # The stream is the "screen" or "display" where one sees the live test execution
            # The result of .run() is a TestResult object that contains:
            #         self.failures = []
            #         self.errors = []
            #         self.testsRun = 0
            #         self.expectedFailures = []
            # ...
            # print(list(os.walk(test_dir, topdown=False)))
            full_output = StringIO()  # todo: maybe change this line
            runner = unittest.TextTestRunner(stream=full_output, verbosity=2)
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

    def get_test_code(self):
        with open('testservice/testing/test_suma.py', 'r') as f:
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




