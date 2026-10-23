# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: tibble_options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 18

suppressPackageStartupMessages(library(tibble))
# Default setting:
getOption("tibble.view_max")

# Change for the duration of the session:
old <- options(tibble.view_max = 100)

# view() would show only 100 rows e.g. for a lazy data frame

# Change back to the original value:
options(old)

# Local scope:
local({
  rlang::local_options(tibble.view_max = 100)
  # view() would show only 100 rows e.g. for a lazy data frame
})
# view() would show the default 1000 rows e.g. for a lazy data frame