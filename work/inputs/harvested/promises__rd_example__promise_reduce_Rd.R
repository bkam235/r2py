# r2py crawler metadata
# package: promises
# source_type: rd_example
# topic: promise_reduce.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\promises\help
# lines: 11

suppressPackageStartupMessages(library(promises))
# Returns a promise for the sum of e1 + e2, with a 0.5 sec delay
slowly_add <- function(e1, e2) {
  promise(\(resolve, reject) {
    later::later(\() resolve(e1 + e2), delay = 0.5)
  })
}

# Prints 55 after a little over 5 seconds
promise_reduce(1:10, slowly_add, .init = 0) |>
  then(print)