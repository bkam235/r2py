# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: plot.svm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 15

suppressPackageStartupMessages(library(e1071))
## a simple example
data(cats, package = "MASS")
m <- svm(Sex~., data = cats)
plot(m, cats)

## more than two variables: fix 2 dimensions
data(iris)
m2 <- svm(Species~., data = iris)
plot(m2, iris, Petal.Width ~ Petal.Length,
     slice = list(Sepal.Width = 3, Sepal.Length = 4))

## plot with custom symbols and colors
plot(m, cats, svSymbol = 1, dataSymbol = 2, symbolPalette = rainbow(4),
color.palette = terrain.colors)