# r2py crawler metadata
# package: broom
# source_type: vignette
# topic: broom_and_dplyr_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\doc\broom_and_dplyr.R
# lines: 12

suppressPackageStartupMessages(library(broom))
knitr::opts_chunk$set(message = FALSE, warning = FALSE)

if (rlang::is_installed("ggplot2")) {
  run <- TRUE
} else {
  run <- FALSE
}

knitr::opts_chunk$set(
  eval = run
)