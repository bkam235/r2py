# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_shift.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 10

suppressPackageStartupMessages(library(forcats))
x <- factor(
  c("Mon", "Tue", "Wed"),
  levels = c("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"),
  ordered = TRUE
)
x
fct_shift(x)
fct_shift(x, 2)
fct_shift(x, -1)