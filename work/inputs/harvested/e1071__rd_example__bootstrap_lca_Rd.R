# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: bootstrap.lca.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 12

suppressPackageStartupMessages(library(e1071))
## Generate a 4-dim. sample with 2 latent classes of 500 data points each.
## The probabilities for the 2 classes are given by type1 and type2.
type1 <- c(0.8, 0.8, 0.2, 0.2)
type2 <- c(0.2, 0.2, 0.8, 0.8)
x <- matrix(runif(4000), nrow = 1000)
x[1:500,] <- t(t(x[1:500,]) < type1) * 1
x[501:1000,] <- t(t(x[501:1000,]) < type2) * 1

l <- lca(x, 2, niter=5)
bl <- bootstrap.lca(l,nsamples=3,lcaiter=5)
bl