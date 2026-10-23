# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: relax_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\relax.R
# lines: 6

library(glmnet)
data(QuickStartExample)
x <- QuickStartExample$x
y <- QuickStartExample$y
fit <- glmnet(x, y, relax = TRUE)
print(fit)