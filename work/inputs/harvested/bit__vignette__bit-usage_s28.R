# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s28
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 12

suppressPackageStartupMessages(library(bit))
l <- c(NA, NA, FALSE, TRUE, TRUE)
b <- as.bit(l)
length(b)
anyNA(b)
any(b)
all(b)
sum(b)
min(b)
max(b)
range(b)
summary(b)