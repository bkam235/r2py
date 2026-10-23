# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: auto_browse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 14

suppressPackageStartupMessages(library(purrr))
# For interactive usage, auto_browse() is useful because it automatically
# starts a browser() in the right place.
f <- function(x) {
  y <- 20
  if (x > 5) {
    stop("!")
  } else {
    x
  }
}
if (interactive()) {
  map(1:6, auto_browse(f))
}