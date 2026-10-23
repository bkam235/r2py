# r2py crawler metadata
# package: glmnet
# source_type: rd_example
# topic: print.cv.glmnet.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\help
# lines: 8

suppressPackageStartupMessages(library(glmnet))
x = matrix(rnorm(100 * 20), 100, 20)
y = rnorm(100)
fit1 = cv.glmnet(x, y)
print(fit1)
fit1r = cv.glmnet(x, y, relax = TRUE)
print(fit1r)
## print.cv.glmnet(fit1r)  ## CHECK WITH TREVOR