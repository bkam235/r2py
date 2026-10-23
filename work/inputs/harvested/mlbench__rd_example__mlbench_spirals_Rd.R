# r2py crawler metadata
# package: mlbench
# source_type: rd_example
# topic: mlbench.spirals.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\mlbench\help
# lines: 8

suppressPackageStartupMessages(library(mlbench))
# 1 cycle each, no noise
p<-mlbench.spirals(300)
plot(p)
#
# 1.5 cycles each, with noise
p<-mlbench.spirals(300,1.5,0.05)
plot(p)