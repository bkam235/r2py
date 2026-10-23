# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s55
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 9

suppressPackageStartupMessages(library(bit))
x = as.integer(c(1, 2, 2, 3, 3, 3))
y = 2:4
union(x, y)
merge_union(x, y, method="unique")
merge_union(x, y, method="exact")
merge_union(x, y, method="all")
sort(c(x, y))
c(x, y)