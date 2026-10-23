# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: duration_precision.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 4

suppressPackageStartupMessages(library(clock))
duration_precision(duration_seconds(1))
duration_precision(duration_nanoseconds(2))
duration_precision(duration_quarters(1:5))