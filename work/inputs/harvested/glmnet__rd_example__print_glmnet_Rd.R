# r2py crawler metadata
# package: glmnet
# source_type: rd_example
# topic: print.glmnet.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\help
# lines: 5

suppressPackageStartupMessages(library(glmnet))
x = matrix(rnorm(100 * 20), 100, 20)
y = rnorm(100)
fit1 = glmnet(x, y)
print(fit1)