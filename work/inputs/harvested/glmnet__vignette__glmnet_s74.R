# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnet_s74
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnet.R
# lines: 7

suppressPackageStartupMessages(library(glmnet))
set.seed(101)
X <- matrix(rnorm(5), nrow = 5)
X2 <- sample(letters[1:3], 5, replace = TRUE)
X3 <- sample(LETTERS[1:3], 5, replace = TRUE)
df <- data.frame(X, X2, X3)
makeX(df)