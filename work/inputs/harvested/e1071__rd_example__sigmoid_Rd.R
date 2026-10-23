# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: sigmoid.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 4

suppressPackageStartupMessages(library(e1071))
plot(sigmoid, -5, 5, ylim = c(-.2, 1))
plot(dsigmoid, -5, 5, add = TRUE, col = 2)
plot(d2sigmoid, -5, 5, add = TRUE, col = 3)