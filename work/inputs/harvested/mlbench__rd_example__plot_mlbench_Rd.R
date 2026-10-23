# r2py crawler metadata
# package: mlbench
# source_type: rd_example
# topic: plot.mlbench.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\mlbench\help
# lines: 8

suppressPackageStartupMessages(library(mlbench))
# 6 normal classes
p <- mlbench.2dnormals(500,6)
plot(p)

# 4-dimensiona XOR
p <- mlbench.xor(500,4)
plot(p)