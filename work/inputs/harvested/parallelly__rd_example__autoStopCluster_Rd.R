# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: autoStopCluster.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 6

suppressPackageStartupMessages(library(parallelly))
cl <- makeClusterPSOCK(2, dryrun = TRUE)
cl <- autoStopCluster(cl)
print(cl)
rm(list = "cl")
gc()