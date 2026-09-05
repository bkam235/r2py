# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd

# R's as_naive_time(year_month_day(...)) effectively creates a time representation.
# In Python, we use Timestamp for calculations and then format as time.
# r2py:entity:from
from_date = pd.Timestamp(2019, 1, 1, 2, 30, 0)

# r2py:entity:to
to_date = pd.Timestamp(2019, 1, 1, 12, 30, 0)

# seq(from, to, by = duration_minutes(90))
# r2py:entity:seq
seq_range = pd.date_range(start=from_date, end=to_date, freq='90min')

# Format to match R's <naive_time<second>> output: "YYYY-MM-DDTHH:MM:SS"
# Note: R's naive_time usually prints the date part if created from year_month_day 
# as seen in the provided R output: "2019-01-01T02:30:00"
formatted_seq = [t.strftime('%Y-%m-%dT%H:%M:%S') for t in seq_range]

# To mimic R's printed output structure
print(f'      <naive_time<second>[{len(formatted_seq)}]>')
for i in range(0, len(formatted_seq), 3):
    chunk = formatted_seq[i:i+3]
    line = ' '.join([f'"{x}"' for x in chunk])
    print(f'[{i+1}] {line}')