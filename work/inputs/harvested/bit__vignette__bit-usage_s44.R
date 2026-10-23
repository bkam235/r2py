# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s44
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 5

suppressPackageStartupMessages(library(bit))
bit_rangediff(c(1L, 7L), (3:5))
bit_rangediff(c(7L, 1L), (3:5))
bit_rangediff(c(1L, 7L), -(3:5), revy=TRUE)
bit_rangediff(c(1L, 7L), -(3:5), revx=TRUE)