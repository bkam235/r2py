# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: duration-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 22

suppressPackageStartupMessages(library(clock))
x <- duration_seconds(5)

# Addition in the same precision
add_seconds(x, 1:10)

# Addition with days, defined as 86400 seconds
add_days(x, 1)

# Similarly, if you start with days and add seconds, you get the common
# precision of the two back, which is seconds
y <- duration_days(1)
add_seconds(y, 5)

# But you can't add a chronological duration (days) and
# a calendrical duration (months)
try(add_months(y, 1))

# You can add years to a duration of months, which adds
# an additional 12 months / year
z <- duration_months(5)
add_years(z, 1)