# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnetFamily_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnetFamily.R
# lines: 10

suppressPackageStartupMessages(library(glmnet))
set.seed(2020)
n <- 100
p <- 4
x <- matrix(runif(n * p, 5, 10), n)
y <- rpois(n, exp(rowMeans(x)))

# glm fit
glmfit <- glm(y ~ x - 1, family = poisson)
coef(glmfit)