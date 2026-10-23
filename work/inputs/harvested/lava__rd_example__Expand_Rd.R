# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: Expand.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 6

suppressPackageStartupMessages(library(lava))
dd <- Expand(iris, Sepal.Length=2:8, Species=c("virginica","setosa"))
summary(dd)

T <- with(warpbreaks, table(wool, tension))
Expand(T)