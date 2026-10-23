# r2py crawler metadata
# package: modelr
# source_type: rd_example
# topic: resample_partition.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\modelr\help
# lines: 5

suppressPackageStartupMessages(library(modelr))
ex <- resample_partition(mtcars, c(test = 0.3, train = 0.7))
mod <- lm(mpg ~ wt, data = ex$train)
rmse(mod, ex$test)
rmse(mod, ex$train)