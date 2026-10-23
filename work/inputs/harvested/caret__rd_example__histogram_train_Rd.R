# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: histogram.train.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 23

suppressPackageStartupMessages(library(caret))
library(mlbench)
data(BostonHousing)

library(rpart)
rpartFit <- train(medv ~ .,
                  data = BostonHousing,
                  "rpart", 
                  tuneLength = 9,
                  trControl = trainControl(
                    method = "boot", 
                    returnResamp = "all"))

densityplot(rpartFit,
            adjust = 1.25)

xyplot(rpartFit,
       metric = "Rsquared",
       type = c("p", "a"))

stripplot(rpartFit,
          horizontal = FALSE,
          jitter = TRUE)