# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: csplit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 5

suppressPackageStartupMessages(library(lava))
foldr(5,2,rep=2)
csplit(10,3)
csplit(iris[1:10,]) ## Split in two sets 1:(n/2) and (n/2+1):n
csplit(iris[1:10,],0.5)