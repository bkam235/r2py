# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: pillar_options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 18

suppressPackageStartupMessages(library(pillar))
if (rlang::is_installed("tibble")) withAutoprint({ # examplesIf
df <- tibble::tibble(x = c(1.234567, NA, 5:10))
df

# Change for the duration of the session:
old <- options(
  pillar.sigfig = 6,
  pillar.print_max = 5,
  pillar.print_min = 5,
  pillar.advice = FALSE
)
df

# Change back to the original value:
options(old)
df
}) # examplesIf