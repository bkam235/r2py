# r2py crawler metadata
# package: future
# source_type: rd_example
# topic: backtrace.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future\help
# lines: 14

suppressPackageStartupMessages(library(future))
my_log <- function(x) log(x)
foo <- function(...) my_log(...)

f <- future({ foo("a") })
res <- tryCatch({
  v <- value(f)
}, error = function(ex) {
  t <- backtrace(f)
  print(t)
})

## R CMD check: make sure any open connections are closed afterward
plan(sequential)