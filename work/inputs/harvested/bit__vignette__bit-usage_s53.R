# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s53
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 10

suppressPackageStartupMessages(library(bit))
x = as.integer(c(0, 1, 2, 2, 3, 3, 3))
y = as.integer(c(1, 2, 3))
setdiff(x, y)
merge_setdiff(x, y)
merge_setdiff(x, y, method="exact")
merge_rangediff(c(0L, 4L), y)
merge_rangediff(c(0L, 4L), c(-3L, -2L)) # y has no effect due to different sign
merge_rangediff(c(0L, 4L), c(-3L, -2L), revy=TRUE)
merge_rangediff(c(0L, 4L), c(-3L, -2L), revx=TRUE)