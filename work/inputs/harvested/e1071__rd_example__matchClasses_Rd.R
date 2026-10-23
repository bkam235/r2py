# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: matchClasses.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 21

suppressPackageStartupMessages(library(e1071))
## a stupid example with no class correlations:
g1 <- sample(1:5, size=1000, replace=TRUE)
g2 <- sample(1:5, size=1000, replace=TRUE)
tab <- table(g1, g2)
matchClasses(tab, "exact")

## let pairs (g1=1,g2=4) and (g1=3,g2=1) agree better
k <- sample(1:1000, size=200)
g1[k] <- 1
g2[k] <- 4

k <- sample(1:1000, size=200)
g1[k] <- 3
g2[k] <- 1

tab <- table(g1, g2)
matchClasses(tab, "exact")

## get agreement coefficients:
compareMatchedClasses(g1, g2, method="exact")