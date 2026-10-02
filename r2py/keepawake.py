"""Keep the machine awake while a long job runs.

On Windows a laptop that goes idle enters Modern Standby and freezes background processes.  The
replay of 2026-10-02 lost 70 minutes that way: three workers went silent together at 12:36 and resumed
together at 13:36:56, the minute the system logged its exit from connected standby (Kernel-Power
event 507).  Calling ``keep_awake()`` at the start of a long script asks Windows not to idle-sleep for
as long as the process lives; elsewhere it does nothing.
"""
from __future__ import annotations

import os

_ES_CONTINUOUS = 0x80000000
_ES_SYSTEM_REQUIRED = 0x00000001


def keep_awake() -> bool:
    """Request that the system stay awake until this process exits; True if the request was made."""
    if os.name != "nt":
        return False
    import ctypes
    return bool(ctypes.windll.kernel32.SetThreadExecutionState(_ES_CONTINUOUS | _ES_SYSTEM_REQUIRED))
