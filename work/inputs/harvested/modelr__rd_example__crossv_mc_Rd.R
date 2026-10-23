# r2py crawler metadata
# package: modelr
# source_type: rd_example
# topic: crossv_mc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\modelr\help
# lines: 9

suppressPackageStartupMessages(library(modelr))
cv1 <- crossv_kfold(mtcars, 5)
cv1

library(purrr)
cv2 <- crossv_mc(mtcars, 100)
models <- map(cv2$train, ~ lm(mpg ~ wt, data = .))
errs <- map2_dbl(models, cv2$test, rmse)
hist(errs)