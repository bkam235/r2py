# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnet_s73
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnet.R
# lines: 6

suppressPackageStartupMessages(library(glmnet))
data(BinomialExample)
x <- BinomialExample$x
y <- BinomialExample$y
fit <- bigGlm(x, y, family = "binomial", lower.limits = -1)
print(fit)