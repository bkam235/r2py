# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnet_s49
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnet.R
# lines: 7

suppressPackageStartupMessages(library(glmnet))
data(BinomialExample)
x <- BinomialExample$x
y <- BinomialExample$y
itrain <- 1:70
fit <- glmnet(x[itrain, ], y[itrain], family = "binomial", nlambda = 5)
assess.glmnet(fit, newx = x[-itrain, ], newy = y[-itrain])