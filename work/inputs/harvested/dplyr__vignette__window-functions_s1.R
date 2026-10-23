# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: window-functions_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\window-functions.R
# lines: 8

knitr::opts_chunk$set(collapse = T, comment = "#>")
options(tibble.print_min = 4L, tibble.print_max = 4L)
library(dplyr)
set.seed(1014)

if (!rlang::is_installed("Lahman")) {
  knitr::opts_chunk$set(eval = FALSE)
}