# r2py crawler metadata
# package: mlbench
# source_type: rd_example
# topic: mlbench.2dnormals.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\mlbench\help
# lines: 7

suppressPackageStartupMessages(library(mlbench))
# 2 classes
p <- mlbench.2dnormals(500,2)
plot(p)
# 6 classes
p <- mlbench.2dnormals(500,6)
plot(p)