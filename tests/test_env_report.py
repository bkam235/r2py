"""R session reports are not scored (user's decision, 2026-10-18): a faithful translation reports Python's
environment, so the comparison measures nothing a translation can do."""
import unittest
from types import SimpleNamespace as NS

from r2py.stage4.verifier import _environment_report_entities


class TestEnvironmentReport(unittest.TestCase):
    def test_session_report_calls_are_found_and_look_alikes_are_not(self):
        src = ("library(sessioninfo)\nsession_info(info = 'all')\nx <- Sys.info()\nmy_session_info_x <- 1\n"
               "sessioninfo::platform_info()\nR.versions <- 2\n")
        ents = {f"e{i}": NS(source_span=NS(start_line=i, end_line=i)) for i in range(6)}
        self.assertEqual(_environment_report_entities(NS(source=src, entities=ents)), {"e1", "e2", "e4"})


if __name__ == "__main__":
    unittest.main()
