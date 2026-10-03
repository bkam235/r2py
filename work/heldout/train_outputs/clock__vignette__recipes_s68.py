# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# x <- zoned_time_parse_complete("2019-01-01T00:00:00-05:00[America/New_York]")
# r2py:entity:x
x = pd.Timestamp("2019-01-01T00:00:00-05:00").tz_convert("America/New_York")

# info <- zoned_time_info(x)
# In Python, timezone information is handled by the pytz library or zoneinfo
# r2py:entity:info
tz = pytz.timezone(str(x.tz))
info = tz

# info$begin
# Approximating the timezone's definition start (the earliest date the zone is defined)
# Note: clock::zoned_time_info provides the internal IANA boundaries. 
# Python's pytz provides the timeline of transitions.
begin = tz._utc_transition_times[0]

# info$end
# Approximating the timezone's definition end
end = tz._utc_transition_times[-1]

print(begin)
print(end)