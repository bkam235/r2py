# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: classAgreement.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 19

suppressPackageStartupMessages(library(e1071))
## no class correlations: both kappa and crand almost zero
g1 <- sample(1:5, size=1000, replace=TRUE)
g2 <- sample(1:5, size=1000, replace=TRUE)
tab <- table(g1, g2)
classAgreement(tab)

## let pairs (g1=1,g2=1) and (g1=3,g2=3) agree better
k <- sample(1:1000, size=200)
g1[k] <- 1
g2[k] <- 1

k <- sample(1:1000, size=200)
g1[k] <- 3
g2[k] <- 3

tab <- table(g1, g2)
## both kappa and crand should be significantly larger than before
classAgreement(tab)