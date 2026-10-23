# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: makeClusterSequential.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 26

suppressPackageStartupMessages(library(parallelly))
if ((getRversion() >= "4.4.0")) withAutoprint({ # examplesIf
library(parallel)

cl <- makeClusterSequential()
print(cl)

y <- parLapply(cl, X = 1:3, fun = sqrt)
str(y)

pid <- Sys.getpid()
print(pid)
y <- clusterEvalQ(cl, Sys.getpid())
str(y)

abc <- 3.14
y <- clusterEvalQ(cl, { abc <- 42; abc })
str(y)
stopifnot(abc == 3.14)

clusterExport(cl, "abc", envir = environment())
rm(abc)
y <- clusterEvalQ(cl, { abc })
str(y)
stopifnot(y[[1]] == 3.14)
}) # examplesIf