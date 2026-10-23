# r2py crawler metadata
# package: DBI
# source_type: vignette
# topic: DBI-arrow_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\doc\DBI-arrow.R
# lines: 14

suppressPackageStartupMessages(library(DBI))
library(knitr)
opts_chunk$set(echo = TRUE)
knitr::opts_chunk$set(error = Sys.getenv("IN_PKGDOWN") != "true" || (getRversion() < "3.5"))

knit_print.data.frame <- function(x, ...) {
  print(head(x, 6))
  if (nrow(x) > 6) {
    cat("Showing 6 out of", nrow(x), "rows.\n")
  }
  invisible(x)
}

registerS3method("knit_print", "data.frame", "knit_print.data.frame")