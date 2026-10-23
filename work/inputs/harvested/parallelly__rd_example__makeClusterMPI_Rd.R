# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: makeClusterMPI.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 8

suppressPackageStartupMessages(library(parallelly))
if (requireNamespace("Rmpi") && requireNamespace("snow")) {
  cl <- makeClusterMPI(2, autoStop = TRUE)
  print(cl)
  y <- parLapply(cl, X = 1:3, fun = sqrt)
  print(y)
  rm(list = "cl")
}