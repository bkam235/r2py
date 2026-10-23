# r2py crawler metadata
# package: future.apply
# source_type: rd_example
# topic: future_kernapply.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future.apply\help
# lines: 7

suppressPackageStartupMessages(library(future.apply))
library(datasets)
library(stats)

X <- EuStockMarkets[, 1:2]
k <- kernel("daniell", 50)  # a long moving average
X_smooth <- future_kernapply(X, k = k)