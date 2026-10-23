# r2py crawler metadata
# package: future
# source_type: rd_example
# topic: reset.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future\help
# lines: 21

suppressPackageStartupMessages(library(future))
## Like mean(), but fails 90% of the time
shaky_mean <- function(x) {
  if (as.double(Sys.time()) %% 1 < 0.90) stop("boom")
  mean(x)
}

x <- rnorm(100)

## Calculate the mean of 'x' with a risk of failing randomly
f <- future({ shaky_mean(x) })

## Relaunch until success
repeat({
  v <- tryCatch(value(f), error = identity)
  if (!inherits(v, "error")) break
  message("Resetting failed future, and retry in 0.1 seconds")
  f <- reset(f)
  Sys.sleep(0.1)
})
cat("mean:", v, "\n")