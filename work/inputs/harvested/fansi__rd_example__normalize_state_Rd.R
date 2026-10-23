# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: normalize_state.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 23

suppressPackageStartupMessages(library(fansi))
normalize_state("hello\033[42;33m world")
normalize_state("hello\033[42;33m world\033[m")
normalize_state("\033[4mhello\033[42;33m world\033[m")

## Superflous codes removed
normalize_state("\033[31;32mhello\033[m")      # only last color prevails
normalize_state("\033[31\033[32mhello\033[m")  # only last color prevails
normalize_state("\033[31mhe\033[49mllo\033[m") # unused closing

## Equivalent normalized sequences compare identical
identical(
  normalize_state("\033[31;32mhello\033[m"),
  normalize_state("\033[31mhe\033[49mllo\033[m")
)
## External SGR will defeat normalization, unless we `carry` it
red <- "\033[41m"
writeLines(
  c(
    paste(red, "he\033[0mllo", "\033[0m"),
    paste(red, normalize_state("he\033[0mllo"), "\033[0m"),
    paste(red, normalize_state("he\033[0mllo", carry=red), "\033[0m")
) )