# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s37
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 10

suppressPackageStartupMessages(library(bit))
x <- c(NA, NA, 1L, 1L, 2L, 3L)
duplicated(x)
bit_duplicated(x, retFUN=as.logical)
bit_duplicated(x, na.rm=NA, retFUN=as.logical)

duplicated(x, incomparables = NA)
bit_duplicated(x, na.rm=FALSE, retFUN=as.logical)

bit_duplicated(x, na.rm=TRUE, retFUN=as.logical)