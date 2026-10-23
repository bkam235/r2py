# r2py crawler metadata
# package: roxygen2
# source_type: rd_example
# topic: roxy_block.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\help
# lines: 14

suppressPackageStartupMessages(library(roxygen2))
# The easiest way to see the structure of a roxy_block is to create one
# using parse_text:
text <- "
  #' This is a title
  #'
  #' @param x,y A number
  #' @export
  f <- function(x, y) x + y
"

# parse_text() returns a list of blocks, so I extract the first
block <- parse_text(text)[[1]]
block