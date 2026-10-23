# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnet_s57
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnet.R
# lines: 8

suppressPackageStartupMessages(library(glmnet))
data(MultinomialExample)
x <- MultinomialExample$x
y <- MultinomialExample$y
set.seed(101)
itrain <- sample(1:500, 400, replace = FALSE)
cfit <- cv.glmnet(x[itrain, ], y[itrain], family = "multinomial")
cnf <- confusion.glmnet(cfit, newx = x[-itrain, ], newy = y[-itrain])