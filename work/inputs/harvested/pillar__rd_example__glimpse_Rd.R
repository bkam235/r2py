# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: glimpse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 6

suppressPackageStartupMessages(library(pillar))
glimpse(mtcars)

if (rlang::is_installed("nycflights13")) withAutoprint({ # examplesIf
glimpse(nycflights13::flights)
}) # examplesIf