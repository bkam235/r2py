# r2py crawler metadata
# package: promises
# source_type: rd_example
# topic: promise_resolve.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\promises\help
# lines: 7

suppressPackageStartupMessages(library(promises))
promise_resolve(mtcars) |>
  then(head) |>
  then(print)

promise_reject("Something went wrong") |>
  catch(tee = TRUE, \(e) message(conditionMessage(e)))