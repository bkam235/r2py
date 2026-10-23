# r2py crawler metadata
# package: glmnet
# source_type: rd_example
# topic: beta_CVX.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\help
# lines: 4

suppressPackageStartupMessages(library(glmnet))
data(QuickStartExample)
x <- QuickStartExample$x; y <- QuickStartExample$y
glmnet(x, y)