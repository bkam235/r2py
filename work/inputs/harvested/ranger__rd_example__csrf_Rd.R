# r2py crawler metadata
# package: ranger
# source_type: rd_example
# topic: csrf.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ranger\help
# lines: 10

suppressPackageStartupMessages(library(ranger))
## Split in training and test data
train.idx <- sample(nrow(iris), 2/3 * nrow(iris))
iris.train <- iris[train.idx, ]
iris.test <- iris[-train.idx, ]

## Run case-specific RF
csrf(Species ~ ., training_data = iris.train, test_data = iris.test, 
     params1 = list(num.trees = 50, mtry = 4), 
     params2 = list(num.trees = 5))