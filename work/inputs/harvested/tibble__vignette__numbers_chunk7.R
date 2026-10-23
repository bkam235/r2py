# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: numbers_chunk7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\numbers.Rmd
# lines: 5

suppressPackageStartupMessages(library(tibble))
#| label: numbers-14
min(num(1:3, label = "$"))
mean(num(1:3, notation = "eng"))
sin(num(1:3, label = "%", scale = 100))