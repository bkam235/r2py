# r2py crawler metadata
# package: promises
# source_type: rd_example
# topic: promise_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\promises\help
# lines: 17

suppressPackageStartupMessages(library(promises))
p1 <- promise(\(resolve, reject) later::later(\() resolve(1), delay = 1))
p2 <- promise(\(resolve, reject) later::later(\() resolve(2), delay = 2))

# Resolves after 1 second, to the value: 1
promise_race(p1, p2) |>
  then(\(x) {
    cat("promise_race:\n")
    str(x)
  })

# Resolves after 2 seconds, to the value: list(1, 2)
promise_all(p1, p2) |>
  then(\(x) {
    cat("promise_all:\n")
    str(x)
  })