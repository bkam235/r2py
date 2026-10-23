# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s59
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 8

suppressPackageStartupMessages(library(bit))
x <- bit_sort(sample(1000, 10))
merge_first(x)
merge_last(x)
merge_firstnotin(c(300L, 600L), x)
merge_firstin(c(300L, 600L), x)
merge_lastin(c(300L, 600L), x)
merge_lastnotin(c(300L, 600L), x)