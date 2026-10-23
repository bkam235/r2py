# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: shortestPaths.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 17

suppressPackageStartupMessages(library(e1071))
## build a graph with 5 nodes
x <- matrix(NA, 5, 5)
diag(x) <- 0
x[1,2] <- 30; x[1,3] <- 10
x[2,4] <- 70; x[2,5] <- 40
x[3,4] <- 50; x[3,5] <- 20
x[4,5] <- 60
x[5,4] <- 10
print(x)

## compute all path lengths
z <- allShortestPaths(x)
print(z)

## the following should give 1 -> 3 -> 5 -> 4
extractPath(z, 1, 4)