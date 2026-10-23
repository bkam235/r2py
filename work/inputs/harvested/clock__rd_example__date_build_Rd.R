# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_build.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 13

suppressPackageStartupMessages(library(clock))
date_build(2019)
date_build(2019, 1:3)

# Generating invalid dates will trigger an error
try(date_build(2019, 1:12, 31))

# You can resolve this with `invalid`
date_build(2019, 1:12, 31, invalid = "previous")

# But this particular case (the last day of the month) is better
# specified as:
date_build(2019, 1:12, "last")