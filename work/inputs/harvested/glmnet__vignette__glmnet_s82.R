# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnet_s82
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnet.R
# lines: 6

suppressPackageStartupMessages(library(glmnet))
data(QuickStartExample)
x <- QuickStartExample$x
y <- QuickStartExample$y
fit <- glmnet(x, y)
length(fit$lambda)  # number of lambda values fit