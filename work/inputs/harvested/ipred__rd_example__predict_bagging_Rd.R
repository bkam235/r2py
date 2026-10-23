# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: predict.bagging.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 16

suppressPackageStartupMessages(library(ipred))
data("Ionosphere", package = "mlbench")
Ionosphere$V2 <- NULL # constant within groups

# nbagg = 10 for performance reasons here
mod <- bagging(Class ~ ., data=Ionosphere)

# out-of-bag estimate

mean(predict(mod) != Ionosphere$Class)

# predictions for the first 10 observations

predict(mod, newdata=Ionosphere[1:10,])

predict(mod, newdata=Ionosphere[1:10,], type="prob")