from unittest import TestCase
from unittest.mock import Mock, patch
from client import Client
from start import validate_files
from query_script import run_cpu_query, run_gpu_query
from server import TasksService
from gpt_split import create_script_split
import pathlib as pl

class FinalProjTests(TestCase):
    server = TasksService()
    client = Client()

    def test_validate_files(self):
        """
        Test the validate_files function from the start module.

        This method tests various combinations of valid and invalid file names and checks that the function returns
        the expected results.
        """
        valid_script = "example_script.txt"
        invalid_script = "not_example_script.txt"

        self.assertEqual(len(validate_files(valid_script, valid_script)), 2)
        self.assertIsNone(validate_files(invalid_script, valid_script))
        self.assertIsNone(validate_files(valid_script, invalid_script))
        self.assertIsNone(validate_files(invalid_script, invalid_script))

    def assertIsFile(self, path):
        """
        Check that a file exists at the given path.

        Args:
            path (str): The path to the file to check.

        Raises:
            AssertionError: If the file does not exist.
        """
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    def test_server_functions_work(self):
        """
        Test the server functions and other utility functions.

        This method tests several functions from different modules, including generate_python_scripts from the server
        module, and run_cpu_query and run_gpu_query from the query_script module. It also checks that files are created
        with the expected contents.
        """
        aws_script = "print(\"hello, AWS!\")"
        gcp_script = "print(\"hello, GCP!\")"

        # Generate Python scripts and check that the files exist.
        self.assertEqual(self.server.generate_python_scripts(aws_script, gcp_script), 0)
        self.assertIsFile("aws_script.py")
        self.assertIsFile("gcp_script.py")

        # Check the contents of the generated files.
        with open("aws_script.py") as f:
            self.assertEqual(f.readline(), "print(\"hello, AWS!\")")
        with open("gcp_script.py") as f:
            self.assertEqual(f.readline(), "print(\"hello, GCP!\")")

        # Check that create_script_split function returns something.
        self.assertIsNotNone(create_script_split())

        # Check that the query functions return something.
        self.assertIsNotNone(run_cpu_query(test=True))
        self.assertIsNotNone(run_gpu_query(test=True))
