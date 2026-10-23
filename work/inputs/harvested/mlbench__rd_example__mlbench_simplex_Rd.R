# r2py crawler metadata
# package: mlbench
# source_type: rd_example
# topic: mlbench.simplex.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\mlbench\help
# lines: 6

suppressPackageStartupMessages(library(mlbench))
p <- mlbench.simplex()
plot(p)

library("lattice")
cloud(x.3~x.1+x.2, groups=classes, data=as.data.frame(p))