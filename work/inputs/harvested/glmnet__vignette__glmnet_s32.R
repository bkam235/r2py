# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnet_s32
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnet.R
# lines: 5

suppressPackageStartupMessages(library(glmnet))
data(MultiGaussianExample)
x <- MultiGaussianExample$x
y <- MultiGaussianExample$y
mfit <- glmnet(x, y, family = "mgaussian")