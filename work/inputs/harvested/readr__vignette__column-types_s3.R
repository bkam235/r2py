# r2py crawler metadata
# package: readr
# source_type: vignette
# topic: column-types_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\doc\column-types.R
# lines: 7

suppressPackageStartupMessages(library(readr))
tricky_dat <- tibble::tibble(
  x = rep(c("", "2"), c(1000, 1)),
  y = "y"
)
tfile <- tempfile("tricky-column-type-guessing-", fileext = ".csv")
write_csv(tricky_dat, tfile)