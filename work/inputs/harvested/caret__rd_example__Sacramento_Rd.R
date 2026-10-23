# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: Sacramento.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 8

suppressPackageStartupMessages(library(caret))
data(Sacramento)

set.seed(955)
in_train <- createDataPartition(log10(Sacramento$price), p = .8, list = FALSE)

training <- Sacramento[ in_train,]
testing  <- Sacramento[-in_train,]