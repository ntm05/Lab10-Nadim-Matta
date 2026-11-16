# tests/test_deploy.py
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import deploy

ROOT = Path(__file__).resolve().parent.parent


class TestDeploy(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.target = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_deploy_copies_files_and_smoke_test_passes(self):
        current = deploy.deploy(ROOT, self.target, "7")
        self.assertTrue((current / "app.py").is_file())
        self.assertTrue((current / "requirements.txt").is_file())
        self.assertIn("build 7", (current / "VERSION").read_text())
        self.assertEqual(deploy.smoke_test(current),
                         "Hello, World from Nadim Matta!")

    def test_redeploy_replaces_current(self):
        deploy.deploy(ROOT, self.target, "1")
        current = deploy.deploy(ROOT, self.target, "2")
        self.assertIn("build 2", (current / "VERSION").read_text())
        self.assertEqual(len(list((self.target / "releases").iterdir())), 2)

    def test_smoke_test_detects_broken_app(self):
        broken = self.target / "broken"
        broken.mkdir()
        (broken / "app.py").write_text("def greet(name):\n    return 'x'\n")
        with self.assertRaises(RuntimeError):
            deploy.smoke_test(broken)

    def test_main(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = deploy.main(["--target", str(self.target),
                                "--build", "42"])
        self.assertEqual(code, 0)
        self.assertIn("Smoke test passed", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
