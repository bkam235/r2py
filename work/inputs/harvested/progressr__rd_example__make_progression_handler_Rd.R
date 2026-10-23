# r2py crawler metadata
# package: progressr
# source_type: rd_example
# topic: make_progression_handler.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\progressr\help
# lines: 20

suppressPackageStartupMessages(library(progressr))
## Create a progression handler that reports on the current progress
## step, the relative change, and the current progress message. This
## is only reported on positive progressions updated
my_handler <- make_progression_handler(name = "my", reporter = list(
  update = function(config, state, progression, ...) {
    if (progression$amount > 0) {
      message(sprintf("step = %d (+%g): message = %s",
                      state$step,
                      progression$amount,
                      sQuote(state$message)))
    }
  }
))

handlers(my_handler)

with_progress({
  y <- slow_sum(1:5)
})