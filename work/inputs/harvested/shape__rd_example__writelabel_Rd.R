# r2py crawler metadata
# package: shape
# source_type: rd_example
# topic: writelabel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shape\help
# lines: 5

suppressPackageStartupMessages(library(shape))
plot(runif(2), main = "writelabel")
writelabel("A")
writelabel("B", at = 0)
writelabel("C", at = 1)