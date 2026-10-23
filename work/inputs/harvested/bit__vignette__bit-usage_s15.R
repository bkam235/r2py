# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 5

suppressPackageStartupMessages(library(bit))
l <- c(FALSE, TRUE, FALSE)
w <- which(l)
w
as.logical(w) # does not coerce back
