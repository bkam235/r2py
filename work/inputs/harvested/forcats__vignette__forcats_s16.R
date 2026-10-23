# r2py crawler metadata
# package: forcats
# source_type: vignette
# topic: forcats_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\doc\forcats.R
# lines: 5

suppressPackageStartupMessages(library(forcats))
reshuffled_income <- gss_cat$rincome |>
  fct_shuffle()

levels(reshuffled_income)