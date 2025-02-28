import os
import tempfile
import unittest
import uuid
from contextlib import contextmanager
from io import StringIO


class CodeTestingService:
    def __init__(self, unique_id):
        self.uuid = unique_id

    @contextmanager # converts the function into a context manager to be used with the 'with' statement
    def create_test_environment(self, submission_code):

        # create unique test dir
        test_dir = os.path.join(tempfile.gettempdir(), f"test_{self.uuid}")
        os.makedirs(test_dir)
        print(test_dir[:20])

        try:
            # create files
            code_path = os.path.join(test_dir, f'solution.py')
            code_test_path = os.path.join(test_dir, f'test_solution.py')

            # write files
            with open(code_path, 'w') as f:
                f.write(submission_code)

            with open(code_test_path, 'w') as f:
                f.write(self.get_test_code())

            yield test_dir

        finally:  # once test_dir has been used, we delete everything
            self.cleanup_directory(test_dir)


    def run_tests(self, submission_code):

        with self.create_test_environment(submission_code) as test_dir:
            loader = unittest.TestLoader()
            # a TestSuite is a collection of test cases, test suites, or both.
            # It is used to aggregate tests that should be executed together.
            suite = loader.discover(test_dir, pattern=f'test_*.py')
            print(suite)
            # run tests with a custom result collector
            # The stream is the "screen" or "display" where one sees the live test execution
            # The result of .run() is a TestResult object that contains:
            #         self.failures = []
            #         self.errors = []
            #         self.testsRun = 0
            #         self.expectedFailures = []
            # ...
            full_output = StringIO()  # todo: maybe change this line
            runner = unittest.TextTestRunner(stream=full_output, verbosity=2)
            result = runner.run(suite)

            return self.format_results(result)

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
        return "from solution import suma as foo\n" + test_code


    @staticmethod
    def format_results(result):
        # input()

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
            'output': result.stream.getvalue()
        }




def test():
    service = CodeTestingService(uuid.uuid4().hex)
    code = """
def aux(x, y):    
    return x + y
    
def suma(a, b):
    
    return a + 1
"""
    test_results = service.run_tests(code)

    print("Results:")
    import json
    print(json.dumps(test_results['output'].split("\n"), indent=4))
    # for key, value in test_results.items():
    #     if key == "output":
    #         continue
    #     print(f"{type(value)}: {key}:")
    #     if type(value) == list or type(value) == tuple:
    #         for item in value:
    #             print(f"{item}\n")
    #     else:
    #         print(f"{value}\n")


# test()