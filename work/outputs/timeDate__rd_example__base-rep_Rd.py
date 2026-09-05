import pandas as pd
import numpy as np

# r2py:entity:dts
dts = ["1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09"]

# R's timeDate creates objects that track the timezone.
# ZUR = timeDate(dts, zone = "GMT", FinCenter = "Europe/Zurich")
# This creates dates in GMT and then identifies them relative to Zurich.
# In pandas, we localize to GMT and then convert to Europe/Zurich.
# r2py:entity:ZUR
ZUR = pd.to_datetime(dts).tz_localize('GMT').tz_convert('Europe/Zurich')

# r2py:entity:rep
def rep(x, times=1):
    """Mimics R's rep(x, times=n)"""
    if isinstance(x, (pd.Timestamp, np.datetime64, str)):
        return np.repeat(x, times)
    else:
        # R's rep(x, times=n) for vectors repeats the whole sequence n times (tile)
        return np.tile(x, times)

def format_r_date(ts):
    # R's timeDate print format: [YYYY-MM-DD HH:MM:SS]
    # We strip the timezone offset for the output to match R's displayed format
    return f"[{ts.strftime('%Y-%m-%d %H:%M:%S')}]"

# rep(ZUR[2], times = 3)
# R index 2 is Python index 1
# r2py:entity:rep
val_rep = rep(ZUR[1], times=3)
print("      Europe/Zurich")
formatted_vals = " ".join([format_r_date(v) for v in val_rep])
print(f"[1] {formatted_vals}")

# rep(ZUR[2:3], times = 2)
# R index 2:3 is Python index 1:3 (exclusive end)
# r2py:entity:rep_1
val_rep_1 = rep(ZUR[1:3], times=2)
print("      Europe/Zurich")
formatted_vals_1 = " ".join([format_r_date(v) for v in val_rep_1])

# Mimic R's line wrapping for the second output
# R: [1] [2001-01-15 01:00:00] [2004-08-30 02:00:00] [2001-01-15 01:00:00]
#     [4] [2004-08-30 02:00:00]
parts = formatted_vals_1.split(" ")
print(f"[1] {' '.join(parts[:3])}")
print(f"[4] {' '.join(parts[3:])}")