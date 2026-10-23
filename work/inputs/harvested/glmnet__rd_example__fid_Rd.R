# r2py crawler metadata
# package: glmnet
# source_type: rd_example
# topic: fid.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\help
# lines: 6

suppressPackageStartupMessages(library(glmnet))
# Example with no ties
glmnet:::fid(c(1, 4, 5, 6), 1:5)

# Example with ties
glmnet:::fid(c(1, 1, 1, 2, 3, 3, 4, 4, 4), 1:9)