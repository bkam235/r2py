# r2py crawler metadata
# package: future.apply
# source_type: rd_example
# topic: future_apply.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future.apply\help
# lines: 42

suppressPackageStartupMessages(library(future.apply))
## ---------------------------------------------------------
## apply()
## ---------------------------------------------------------
X <- matrix(c(1:4, 1, 6:8), nrow = 2L)

Y0 <- apply(X, MARGIN = 1L, FUN = table)
Y1 <- future_apply(X, MARGIN = 1L, FUN = table)
print(Y1)
stopifnot(all.equal(Y1, Y0, check.attributes = FALSE)) ## FIXME

Y0 <- apply(X, MARGIN = 1L, FUN = stats::quantile)
Y1 <- future_apply(X, MARGIN = 1L, FUN = stats::quantile)
print(Y1)
stopifnot(all.equal(Y1, Y0))


## ---------------------------------------------------------
## Parallel Random Number Generation
## ---------------------------------------------------------

## Regardless of the future plan, the number of workers, and
## where they are, the random numbers produced are identical

X <- matrix(c(1:4, 1, 6:8), nrow = 2L)

plan(multisession)
set.seed(0xBEEF)
Y1 <- future_apply(X, MARGIN = 1L, FUN = sample, future.seed = TRUE)
print(Y1)

plan(sequential)
set.seed(0xBEEF)
Y2 <- future_apply(X, MARGIN = 1L, FUN = sample, future.seed = TRUE)
print(Y2)

stopifnot(all.equal(Y1, Y2))



## R CMD check: make sure any open connections are closed afterward
if (!inherits(plan(), "sequential")) plan(sequential)