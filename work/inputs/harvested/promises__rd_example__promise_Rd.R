# r2py crawler metadata
# package: promises
# source_type: rd_example
# topic: promise.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\promises\help
# lines: 16

suppressPackageStartupMessages(library(promises))
# Create a promise that resolves to a random value after 2 secs
p1 <- promise(\(resolve, reject) {
  later::later(\() resolve(runif(1)), delay = 2)
})

p1 |> then(print)

# Create a promise that errors immediately
p2 <- promise(\(resolve, reject) {
  reject("An error has occurred")
})
then(p2,
  onFulfilled = \(value) message("Success"),
  onRejected = \(err) message("Failure")
)