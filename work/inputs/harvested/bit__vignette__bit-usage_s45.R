# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s45
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 4

suppressPackageStartupMessages(library(bit))
bit_rangediff(c(1L, 7L), (1:7))
bit_rangediff(c(1L, 7L), -(1:7))
bit_rangediff(c(1L, 7L), (1:7), revy=TRUE)