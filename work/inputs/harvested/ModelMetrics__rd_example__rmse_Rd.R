# r2py crawler metadata
# package: ModelMetrics
# source_type: rd_example
# topic: rmse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ModelMetrics\help
# lines: 6

suppressPackageStartupMessages(library(ModelMetrics))
data(testDF)
glmModel <- glm(y ~ ., data = testDF, family="binomial")
Preds <- predict(glmModel, type = 'response')

rmse(testDF$y, Preds)