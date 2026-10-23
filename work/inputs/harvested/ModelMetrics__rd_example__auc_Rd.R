# r2py crawler metadata
# package: ModelMetrics
# source_type: rd_example
# topic: auc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ModelMetrics\help
# lines: 8

suppressPackageStartupMessages(library(ModelMetrics))
data(testDF)
glmModel <- glm(y ~ ., data = testDF, family="binomial")
Preds <- predict(glmModel, type = 'response')

auc(testDF$y, Preds)
# using s3 method for glm
auc(glmModel)