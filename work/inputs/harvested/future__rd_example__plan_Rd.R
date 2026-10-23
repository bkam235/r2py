# r2py crawler metadata
# package: future
# source_type: rd_example
# topic: plan.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future\help
# lines: 86

suppressPackageStartupMessages(library(future))
a <- b <- c <- NA_real_

# An sequential future
plan(sequential)
f <- future({
  a <- 7
  b <- 3
  c <- 2
  a * b * c
})
y <- value(f)
print(y)
str(list(a = a, b = b, c = c)) ## All NAs


# A sequential future with lazy evaluation
plan(sequential)
f <- future({
  a <- 7
  b <- 3
  c <- 2
  a * b * c
}, lazy = TRUE)
y <- value(f)
print(y)
str(list(a = a, b = b, c = c)) ## All NAs


# A multicore future (specified as a string)
plan("multicore")
f <- future({
  a <- 7
  b <- 3
  c <- 2
  a * b * c
})
y <- value(f)
print(y)
str(list(a = a, b = b, c = c)) ## All NAs

## Multisession futures gives an error on R CMD check on
## Windows (but not Linux or macOS) for unknown reasons.
## The same code works in package tests.


# A multisession future (specified via a string variable)
plan("future::multisession")
f <- future({
  a <- 7
  b <- 3
  c <- 2
  a * b * c
})
y <- value(f)
print(y)
str(list(a = a, b = b, c = c)) ## All NAs




## Explicitly specifying number of workers
## (default is parallelly::availableCores())
plan(multicore, workers = 2)
message("Number of parallel workers: ", nbrOfWorkers())


## Explicitly close multisession workers by switching plan
plan(sequential)
# Evaluate a future using the 'multisession' plan
with(plan(multisession, workers = 2), {
  f <- future(Sys.getpid())
  w_pid <- value(f)
})
print(c(main = Sys.getpid(), worker = w_pid))



# Evaluate a future locally using the 'multisession' plan
local({
  with(plan(multisession, workers = 2), local = TRUE)

  f <- future(Sys.getpid())
  w_pid <- value(f)
  print(c(main = Sys.getpid(), worker = w_pid))
})