# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: skipping_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\skipping.R
# lines: 8

suppressPackageStartupMessages(library(testthat))
skip_if_dangerous <- function() {
  if (!identical(Sys.getenv("DANGER"), "")) {
    skip("Not run in dangerous environments.")
  } else {
    invisible()
  }
}