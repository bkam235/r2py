# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: as.cluster.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 5

suppressPackageStartupMessages(library(parallelly))
cl1 <- makeClusterPSOCK(2, dryrun = TRUE)
cl2 <- makeClusterPSOCK(c("n1", "server.remote.org"), dryrun = TRUE)
cl <- c(cl1, cl2)
print(cl)