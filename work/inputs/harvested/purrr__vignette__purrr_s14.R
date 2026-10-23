# r2py crawler metadata
# package: purrr
# source_type: vignette
# topic: purrr_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\doc\purrr.R
# lines: 4

suppressPackageStartupMessages(library(purrr))
xs <- map(1:8, ~ runif(10))
xs[[1]][[1]] <- NA
ws <- map(1:8, ~ rpois(10, 5) + 1)