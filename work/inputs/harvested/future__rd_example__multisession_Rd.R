# r2py crawler metadata
# package: future
# source_type: rd_example
# topic: multisession.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future\help
# lines: 26

suppressPackageStartupMessages(library(future))
## Use multisession futures
plan(multisession)

## A global variable
a <- 0

## Create future (explicitly)
f <- future({
  b <- 3
  c <- 2
  a * b * c
})

## A multisession future is evaluated in a separate R session.
## Changing the value of a global variable will not affect
## the result of the future.
a <- 7
print(a)

v <- value(f)
print(v)
stopifnot(v == 0)

## Explicitly close multisession workers by switching plan
plan(sequential)