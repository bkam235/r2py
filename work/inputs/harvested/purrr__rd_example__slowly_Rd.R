# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: slowly.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 8

suppressPackageStartupMessages(library(purrr))
# For these example, we first create a custom rate
# with a low waiting time between attempts:
rate <- rate_delay(0.1)

# slowly() causes a function to sleep for a given time between calls:
slow_runif <- slowly(\(x) runif(1), rate = rate, quiet = FALSE)
out <- map(1:5, slow_runif)