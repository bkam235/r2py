# r2py crawler metadata
# package: forcats
# source_type: vignette
# topic: forcats_chunk6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\doc\forcats.Rmd
# lines: 4

suppressPackageStartupMessages(library(forcats))
f <- factor(c("x", "y", NA), exclude = NULL)
    levels(f)
    is.na(f)