# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 7

suppressPackageStartupMessages(library(bit))
w <- bitwhich(3, 2)
length(w) <- 6
w
w <- bitwhich(3, -2)
length(w) <- 6
w