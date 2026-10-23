# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 4

suppressPackageStartupMessages(library(bit))
x <- bit(1e6)
y <- x | as.bit(c(FALSE, TRUE))
object.size(y) / object.size(x)