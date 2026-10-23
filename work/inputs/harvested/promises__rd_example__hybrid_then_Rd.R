# r2py crawler metadata
# package: promises
# source_type: rd_example
# topic: hybrid_then.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\promises\help
# lines: 49

suppressPackageStartupMessages(library(promises))
# Basic usage - works with both sync and async values
add_to <- function(x, k) {
  hybrid_then(
    x,
    on_success = function(value) {
      value + k
    },
    on_failure = function(err) {
      message("Error: ", err$message)
      NA_real_
    }
  )
}

# Synchronous
42 |> add_to(100)
#> [1] 142

# Synchronous error
add_to({stop("Bad input!")}, 8)
#> Error: Bad input!
#> [1] NA


# Asynchronous
promise_resolve(42) |>
  add_to(8) |>
  then(print)
# When resolved...
#> [1] 50

# Error handling - asynchronous
promise_resolve(stop("Bad async input!")) |>
  add_to(8) |>
  then(print)
# When resolved...
#> Error: Bad async input!
#> [1] NA

# Chaining multiple operations
# (Move the `promise_resolve()` around to see sync vs async behavior)
1 |>
  hybrid_then(on_success = \(x) x + 1) |>
  hybrid_then(on_success = \(x) promise_resolve(x * 2)) |>
  hybrid_then(on_success = \(x) x - 1) |>
  hybrid_then(print)
# When resolved...
#> [1] 3