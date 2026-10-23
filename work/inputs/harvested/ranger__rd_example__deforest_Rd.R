# r2py crawler metadata
# package: ranger
# source_type: rd_example
# topic: deforest.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ranger\help
# lines: 10

suppressPackageStartupMessages(library(ranger))
## Example of deforesting a random forest
rfo <- ranger(Species ~ ., data = iris, probability = TRUE, num.trees = 100)
dfo <- deforest(rfo, which.trees = c(1, 3, 5))
dfo  # same as `rfo` but with trees 1, 3, and 5 removed

## Sanity check
preds.rfo <- predict(rfo, data = iris, predict.all = TRUE)$predictions
preds.dfo <- predict(dfo, data = iris, predict.all = TRUE)$predictions
identical(preds.rfo[, , -c(1, 3, 5)], y = preds.dfo)