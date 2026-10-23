# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: extending_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\extending.R
# lines: 14

suppressPackageStartupMessages(library(roxygen2))
text <- "
  #' This is a title
  #'
  #' This is the description.
  #'
  #' @param x,y A number
  #' @export
  f <- function(x, y) x + y
"

# parse_text() returns a list of blocks, so I extract the first
block <- parse_text(text)[[1]]
block