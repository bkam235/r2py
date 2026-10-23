# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: rate-helpers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 9

suppressPackageStartupMessages(library(purrr))
# A delay rate waits the same amount of time:
rate <- rate_delay(0.02)
for (i in 1:3) rate_sleep(rate, quiet = FALSE)

# A backoff rate waits exponentially longer each time, with random
# jitter by default:
rate <- rate_backoff(pause_base = 0.2, pause_min = 0.005)
for (i in 1:3) rate_sleep(rate, quiet = FALSE)