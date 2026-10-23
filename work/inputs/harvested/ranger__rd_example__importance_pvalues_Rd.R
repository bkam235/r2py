# r2py crawler metadata
# package: ranger
# source_type: rd_example
# topic: importance_pvalues.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ranger\help
# lines: 12

suppressPackageStartupMessages(library(ranger))
## Janitza's p-values with corrected Gini importance
n <- 50
p <- 400
dat <- data.frame(y = factor(rbinom(n, 1, .5)), replicate(p, runif(n)))
rf.sim <- ranger(y ~ ., dat, importance = "impurity_corrected")
importance_pvalues(rf.sim, method = "janitza")

## Permutation p-values 

rf.iris <- ranger(Species ~ ., data = iris, importance = 'permutation')
importance_pvalues(rf.iris, method = "altmann", formula = Species ~ ., data = iris)