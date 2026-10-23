# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-sequence.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 49

suppressPackageStartupMessages(library(clock))
from <- date_build(2019, 1)
to <- date_build(2019, 4)

# Defaults to daily sequence
date_seq(from, to = to, by = 7)

# Use durations to change to monthly or yearly sequences
date_seq(from, to = to, by = duration_months(1))
date_seq(from, by = duration_years(-2), total_size = 3)

# Note that components of `to` more precise than the precision of `by`
# must match `from` exactly. For example, this is not well defined:
from <- date_build(2019, 5, 2)
to <- date_build(2025, 7, 5)
try(date_seq(from, to = to, by = duration_years(1)))

# The month and day components of `to` must match `from`
to <- date_build(2025, 5, 2)
date_seq(from, to = to, by = duration_years(1))

# ---------------------------------------------------------------------------

# Invalid dates must be resolved with the `invalid` argument
from <- date_build(2019, 1, 31)
to <- date_build(2019, 12, 31)

try(date_seq(from, to = to, by = duration_months(1)))
date_seq(from, to = to, by = duration_months(1), invalid = "previous")

# Compare this to the base R result, which is often a source of confusion
seq(from, to = to, by = "1 month")

# This is equivalent to the overflow invalid resolution strategy
date_seq(from, to = to, by = duration_months(1), invalid = "overflow")

# ---------------------------------------------------------------------------

# Usage of `to` and `total_size` must generate a non-fractional sequence
# between `from` and `to`
from <- date_build(2019, 1, 1)
to <- date_build(2019, 1, 4)

# These are fine
date_seq(from, to = to, total_size = 2)
date_seq(from, to = to, total_size = 4)

# But this is not!
try(date_seq(from, to = to, total_size = 3))