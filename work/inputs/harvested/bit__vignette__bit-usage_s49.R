# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s49
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 5

suppressPackageStartupMessages(library(bit))
x <- sample(9, 9, TRUE)
unique(sort(x))
sort(unique(x))
bit_sort_unique(x)