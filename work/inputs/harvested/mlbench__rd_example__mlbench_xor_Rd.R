# r2py crawler metadata
# package: mlbench
# source_type: rd_example
# topic: mlbench.xor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\mlbench\help
# lines: 8

suppressPackageStartupMessages(library(mlbench))
# 2d example
p<-mlbench.xor(300,2)
plot(p)
#
# 3d example
p<-mlbench.xor(300,3)
plot(p)