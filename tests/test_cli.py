import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

from toolkit.__main__ import main


def run_cli(args):
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class TestCli(unittest.TestCase):
    def test_calc_success(self):
        code, out, err = run_cli(["calc", "2 + 3 * 4"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "14.0")
        self.assertEqual(err, "")

    def test_convert_success(self):
        code, out, err = run_cli(["convert", "1", "--from", "km", "--to", "m"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "1000.0")
        self.assertEqual(err, "")

    def test_calc_error(self):
        code, out, err = run_cli(["calc", "3 +"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("Error", err)

    def test_calc_division_by_zero(self):
        code, out, err = run_cli(["calc", "5 / 0"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("Error", err)

    def test_convert_error(self):
        code, out, err = run_cli(["convert", "5", "--from", "km", "--to", "kg"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("Error", err)

    def test_no_command(self):
        with self.assertRaises(SystemExit) as cm:
            run_cli([])
        self.assertEqual(cm.exception.code, 2)

    def test_convert_without_to(self):
        with self.assertRaises(SystemExit) as cm:
            run_cli(["convert", "5", "--from", "km"])
        self.assertEqual(cm.exception.code, 2)

    def test_help(self):
        with self.assertRaises(SystemExit) as cm:
            run_cli(["--help"])
        self.assertEqual(cm.exception.code, 0)


class TestCliSubprocess(unittest.TestCase):
    def test_calc_process(self):
        r = subprocess.run(
            [sys.executable, "-m", "toolkit", "calc", "2+2"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "4.0")

    def test_error_process(self):
        r = subprocess.run(
            [sys.executable, "-m", "toolkit", "calc", "3 +"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stdout, "")
        self.assertNotEqual(r.stderr, "")


if __name__ == "__main__":
    unittest.main()
