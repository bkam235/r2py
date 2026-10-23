# r2py crawler metadata
# package: mlbench
# source_type: rd_example
# topic: bayesclass.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\mlbench\help
# lines: 6

suppressPackageStartupMessages(library(mlbench))
# 6 overlapping classes
p <- mlbench.2dnormals(500,6)
plot(p)

plot(p$x, col=as.numeric(bayesclass(p)))