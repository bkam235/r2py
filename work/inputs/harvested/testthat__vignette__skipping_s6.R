# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: skipping_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\skipping.R
# lines: 4

suppressPackageStartupMessages(library(testthat))
is_testing <- function() {
  identical(Sys.getenv("TESTTHAT"), "true")
}