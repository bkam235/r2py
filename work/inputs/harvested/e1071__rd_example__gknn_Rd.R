# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: gknn.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 13

suppressPackageStartupMessages(library(e1071))
data(iris)

model <- gknn(Species ~ ., data = iris)
predict(model, iris[c(1, 51, 101),])

test = c(45:50, 95:100, 145:150)

model <- gknn(Species ~ ., data = iris[-test,], k = 3, method = "Manhattan")
predict(model, iris[test,], type = "votes")

model <- gknn(Species ~ ., data = iris[-test], k = 3, method = "Manhattan")
predict(model, iris[test,], type = "prob")