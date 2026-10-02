import unittest
from unittest.mock import MagicMock, patch

from r2py import keepawake


class TestKeepAwake(unittest.TestCase):
    def test_noop_off_windows(self):
        with patch.object(keepawake.os, "name", "posix"):
            self.assertFalse(keepawake.keep_awake())

    def test_requests_continuous_system_required_on_windows(self):
        k32 = MagicMock()
        k32.SetThreadExecutionState.return_value = 0x80000000
        with patch.object(keepawake.os, "name", "nt"), patch("ctypes.windll", create=True) as w:
            w.kernel32 = k32
            self.assertTrue(keepawake.keep_awake())
        k32.SetThreadExecutionState.assert_called_once_with(0x80000001)


if __name__ == "__main__":
    unittest.main()
