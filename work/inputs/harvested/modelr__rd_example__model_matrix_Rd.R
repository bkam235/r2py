# r2py crawler metadata
# package: modelr
# source_type: rd_example
# topic: model_matrix.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\modelr\help
# lines: 4

suppressPackageStartupMessages(library(modelr))
model_matrix(mtcars, mpg ~ cyl)
model_matrix(iris, Sepal.Length ~ Species)
model_matrix(iris, Sepal.Length ~ Species - 1)