# r2py crawler metadata
# package: pillar
# source_type: vignette
# topic: printing_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\doc\printing.R
# lines: 4

suppressPackageStartupMessages(library(pillar))
tbl <- tibble::tibble(a = 1:3, b = tibble::tibble(c = 4:6, d = 7:9), e = 10:12)
print(tbl, width = 23)
str(tbl)