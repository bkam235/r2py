# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: Coxnet_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\Coxnet.R
# lines: 4

suppressPackageStartupMessages(library(glmnet))
try({
fit <- glmnet(x, y3, family = "cox")
})