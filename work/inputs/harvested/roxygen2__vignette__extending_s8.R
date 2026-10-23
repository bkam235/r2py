# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: extending_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\extending.R
# lines: 15

suppressPackageStartupMessages(library(roxygen2))
text <- "
  #' Title
  #'
  #' @tip The mean of a logical vector is the proportion of `TRUE` values.
  #' @tip You can compute means of dates and date-times!
  #' @md
  f <- function(x, y) {
    # ...
  }
"
block <- parse_text(text)[[1]]
block

str(block$tags[[2]])