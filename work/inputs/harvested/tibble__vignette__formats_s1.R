# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: formats_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\formats.R
# lines: 7

suppressPackageStartupMessages(library(tibble))
knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>",
  eval = rlang::is_installed(c("dplyr", "formattable", "ggplot2", "tidyr")),
  error = (Sys.getenv("IN_PKGDOWN") == "")
)