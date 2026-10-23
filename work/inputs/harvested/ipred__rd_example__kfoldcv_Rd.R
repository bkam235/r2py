# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: kfoldcv.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 11

suppressPackageStartupMessages(library(ipred))
# 10-fold CV with N = 91

kfoldcv(10, 91)	


k <- sample(5:15, 1)
k
N <- sample(50:150, 1)
N
stopifnot(sum(kfoldcv(k, N)) == N)