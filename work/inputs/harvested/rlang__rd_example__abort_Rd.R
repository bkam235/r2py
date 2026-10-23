# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: abort.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 71

suppressPackageStartupMessages(library(rlang))
# These examples are guarded to avoid throwing errors
if (FALSE) {

# Signal an error with a message just like stop():
abort("The error message.")


# Unhandled errors are saved automatically by `abort()` and can be
# retrieved with `last_error()`. The error prints with a simplified
# backtrace:
f <- function() try(g())
g <- function() evalq(h())
h <- function() abort("Tilt.")
last_error()

# Use `summary()` to print the full backtrace and the condition fields:
summary(last_error())


# Give a class to the error:
abort("The error message", "mypkg_bad_error")

# This allows callers to handle the error selectively
tryCatch(
  mypkg_function(),
  mypkg_bad_error = function(err) {
    warn(conditionMessage(err)) # Demote the error to a warning
    NA                          # Return an alternative value
  }
)

# You can also specify metadata that will be stored in the condition:
abort("The error message.", "mypkg_bad_error", data = 1:10)

# This data can then be consulted by user handlers:
tryCatch(
  mypkg_function(),
  mypkg_bad_error = function(err) {
    # Compute an alternative return value with the data:
    recover_error(err$data)
  }
)


# If you call low-level APIs it may be a good idea to create a
# chained error with the low-level error wrapped in a more
# user-friendly error. Use `try_fetch()` to fetch errors of a given
# class and rethrow them with the `parent` argument of `abort()`:
file <- "http://foo.bar/baz"
try(
  try_fetch(
    download(file),
    error = function(err) {
      msg <- sprintf("Can't download `%s`", file)
      abort(msg, parent = err)
  })
)

# You can also hard-code the call when it's not easy to
# forward it from the caller
 f <- function() {
  abort("my message", call = call("my_function"))
}
g <- function() {
  f()
}
# Shows that the error occurred in `my_function()`
try(g())

}