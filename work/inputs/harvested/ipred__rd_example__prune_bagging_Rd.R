# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: prune.bagging.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 7

suppressPackageStartupMessages(library(ipred))
data("Glass", package = "mlbench")
library("rpart")

mod <- bagging(Type ~ ., data=Glass, nbagg=10, coob=TRUE)
pmod <- prune(mod)
print(pmod)