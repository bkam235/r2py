# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: insistently.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 43

suppressPackageStartupMessages(library(purrr))
# For the purpose of this example, we first create a custom rate
# object with a low waiting time between attempts:
rate <- rate_delay(0.1)

# insistently() makes a function repeatedly try to work
risky_runif <- function(lo = 0, hi = 1) {
  y <- runif(1, lo, hi)
  if(y < 0.9) {
    stop(y, " is too small")
  }
  y
}

# Let's now create an exponential backoff rate with a low waiting
# time between attempts:
rate <- rate_backoff(pause_base = 0.1, pause_min = 0.005, max_times = 4)

# Modify your function to run insistently.
insistent_risky_runif <- insistently(risky_runif, rate, quiet = FALSE)

set.seed(6) # Succeeding seed
insistent_risky_runif()

set.seed(3) # Failing seed
try(insistent_risky_runif())

# You can also use other types of rate settings, like a delay rate
# that waits for a fixed amount of time. Be aware that a delay rate
# has an infinite amount of attempts by default:
rate <- rate_delay(0.2, max_times = 3)
insistent_risky_runif <- insistently(risky_runif, rate = rate, quiet = FALSE)
try(insistent_risky_runif())

# insistently() and possibly() are a useful combination
rate <- rate_backoff(pause_base = 0.1, pause_min = 0.005)
possibly_insistent_risky_runif <- possibly(insistent_risky_runif, otherwise = -99)

set.seed(6)
possibly_insistent_risky_runif()

set.seed(3)
possibly_insistent_risky_runif()