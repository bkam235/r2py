# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: numbers_chunk3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\numbers.Rmd
# lines: 7

suppressPackageStartupMessages(library(tibble))
#| label: numbers-3
tibble(x = 123.4567)
old <- options(pillar.sigfig = 7)
tibble(x = 123.4567)
# Restore old options, see also rlang::local_options() for a more elegant way
options(old)