# r2py crawler metadata
# package: future
# source_type: rd_example
# topic: makeClusterFuture.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future\help
# lines: 15

suppressPackageStartupMessages(library(future))
if ((getRversion() >= "4.4.0")) withAutoprint({ # examplesIf
plan(multisession)
cl <- makeClusterFuture()

parallel::clusterSetRNGStream(cl)

y <- parallel::parLapply(cl, 11:13, function(x) {
  message("Process ID: ", Sys.getpid())
  mean(rnorm(n = x))
})
str(y)

plan(sequential)
}) # examplesIf