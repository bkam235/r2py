# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: third-edition_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\third-edition.R
# lines: 9

suppressPackageStartupMessages(library(testthat))
f <- function() {
  warning("First warning")
  warning("Second warning")
  warning("Third warning")
}

local_edition(2)
expect_warning(f(), "First")