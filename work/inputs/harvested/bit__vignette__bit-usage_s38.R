# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s38
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 9

suppressPackageStartupMessages(library(bit))
x <- c(NA, NA, 1L, 1L, 2L, 3L)
unique(x)
bit_unique(x)

unique(x, incomparables = NA)
bit_unique(x, na.rm=FALSE)

bit_unique(x, na.rm=TRUE)