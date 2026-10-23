# r2py crawler metadata
# package: promises
# source_type: rd_example
# topic: promise_map.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\promises\help
# lines: 13

suppressPackageStartupMessages(library(promises))
# Waits x seconds, then returns x*10
wait_this_long <- function(x) {
  promise(\(resolve, reject) {
    later::later(\() resolve(x*10), delay = x)
  })
}

promise_map(
  list(A=1, B=2, C=3),
  wait_this_long
) |>
  then(print)