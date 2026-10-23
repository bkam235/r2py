# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: ipredknn.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 9

suppressPackageStartupMessages(library(ipred))
library("mlbench")
learn <- as.data.frame(mlbench.twonorm(300))

mypredict.knn <- function(object, newdata) 
                   predict.ipredknn(object, newdata, type="class")

errorest(classes ~., data=learn, model=ipredknn, 
         predict=mypredict.knn)