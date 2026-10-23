# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s52
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 6

suppressPackageStartupMessages(library(bit))
x = as.integer(c(3, 4, 4, 5))
y = as.integer(c(3, 4, 5))
setequal(x, y)
merge_setequal(x, y)
merge_setequal(x, y, method="exact")