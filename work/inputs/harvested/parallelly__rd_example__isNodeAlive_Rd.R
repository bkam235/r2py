# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: isNodeAlive.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 8

suppressPackageStartupMessages(library(parallelly))
cl <- makeClusterPSOCK(2)

## Check if cluster node #2 is alive
print(isNodeAlive(cl[[2]]))

## Check all nodes
print(isNodeAlive(cl))