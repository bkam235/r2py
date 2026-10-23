# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: fplot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 5

suppressPackageStartupMessages(library(lava))
if (interactive()) {
data(iris)
fplot(Sepal.Length ~ Petal.Length+Species, data=iris, size=2, type="s")
}