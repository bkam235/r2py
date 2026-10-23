# r2py crawler metadata
# package: systemfonts
# source_type: vignette
# topic: systemfonts_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\doc\systemfonts.R
# lines: 16

suppressPackageStartupMessages(library(systemfonts))
google <- suppressWarnings(try(readLines("https://8.8.8.8", n = 1L), silent = TRUE))
is_online <- !inherits(google, "try-error")

knitr::opts_chunk$set(
  dev = "ragg_png",
  dpi = 144,
  collapse = TRUE,
  comment = "#>",
  fig.asp = NULL,
  fig.height = 4.326,
  fig.width = 7,
  eval = is_online
)

systemfonts::require_font("Spectral", fallback = "serif")