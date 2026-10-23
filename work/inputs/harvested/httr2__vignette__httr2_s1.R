# r2py crawler metadata
# package: httr2
# source_type: vignette
# topic: httr2_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\doc\httr2.R
# lines: 10

suppressPackageStartupMessages(library(httr2))
# needs pipe & avoids error = TRUE problem in 4.3.0
run_code <- getRversion() >= "4.4.0"

knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>",
  eval = run_code,
  purl = run_code
)