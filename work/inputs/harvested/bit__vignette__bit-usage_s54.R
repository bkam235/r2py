# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s54
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 8

suppressPackageStartupMessages(library(bit))
x = -2:1
y = -1:2
setdiff(x, y)
union(setdiff(x, y), setdiff(y, x))
merge_symdiff(x, y)
merge_intersect(x, y)
merge_rangesect(c(-2L, 1L), y)