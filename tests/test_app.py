# tests/test_app.py
import io
import runpy
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from app import greet

APP = Path(__file__).resolve().parent.parent / "app.py"


class TestApp(unittest.TestCase):

    def test_greet(self):
        self.assertEqual(greet("World"), "Hello, World from Nadim Matta!")

    def test_greet_other_name(self):
        self.assertEqual(greet("Jenkins"), "Hello, Jenkins from Nadim Matta!")

    def test_main_prints_greeting(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            runpy.run_path(str(APP), run_name="__main__")
        self.assertEqual(buf.getvalue().strip(),
                         "Hello, World from Nadim Matta!")


if __name__ == "__main__":
    unittest.main()
