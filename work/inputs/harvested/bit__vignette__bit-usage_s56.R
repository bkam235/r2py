# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s56
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 5

suppressPackageStartupMessages(library(bit))
x = 2:4
y = as.integer(c(0, 1, 2, 2, 3, 3, 3))
match(x, y)
merge_match(x, y)