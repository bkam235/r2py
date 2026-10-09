"""A file the harness stages for the program (the data-shim sidecar) is an input, not a file the program wrote."""
import json
import tempfile
import unittest
from pathlib import Path

from r2py.stage0.sandbox.py_sandbox import PySandbox
from r2py.types import EffectClass

READS_ONLY = (
    "import json\n"
    "from pathlib import Path\n"
    "d = json.loads((Path(__file__).parent / 'demo.r2py_data.json').read_text(encoding='utf-8'))\n"
    "print(d['x'])\n"
)


class TestSidecarIsNotAWrittenFile(unittest.TestCase):
    def run_py(self, source):
        with tempfile.TemporaryDirectory() as d:
            return PySandbox().run(source, workdir=Path(d), capture=frozenset({EffectClass.FILES, EffectClass.STDOUT}),
                                   timeout_s=60, sidecar_files={"demo.r2py_data.json": json.dumps({"x": 42})})

    def test_reading_the_staged_sidecar_writes_nothing(self):
        b = self.run_py(READS_ONLY)
        self.assertEqual(b.exit_code, 0, b.stderr)
        self.assertIn("42", b.stdout)
        self.assertEqual(b.files, {})

    def test_a_file_the_program_does_write_is_still_captured(self):
        b = self.run_py(READS_ONLY + "Path('out.txt').write_text('hi')\n")
        self.assertEqual(list(b.files), ["out.txt"])


if __name__ == "__main__":
    unittest.main()
