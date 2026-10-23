# r2py crawler metadata
# package: magrittr
# source_type: vignette
# topic: tradeoffs_chunk9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\doc\tradeoffs.Rmd
# lines: 5

suppressPackageStartupMessages(library(magrittr))
sample(10) %>% list(., .)

# Becomes
list(sample(10), sample(10))