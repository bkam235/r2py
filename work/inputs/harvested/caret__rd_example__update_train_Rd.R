# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: update.train.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 12

suppressPackageStartupMessages(library(caret))
data(iris)
TrainData <- iris[,1:4]
TrainClasses <- iris[,5]

knnFit1 <- train(TrainData, TrainClasses,
                 method = "knn",
                 preProcess = c("center", "scale"),
                 tuneLength = 10,
                 trControl = trainControl(method = "cv"))

update(knnFit1, list(.k = 3))