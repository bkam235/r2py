# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: extending_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\extending.R
# lines: 15

suppressPackageStartupMessages(library(roxygen2))
roxy_tag_parse.roxy_tag_memo <- function(x) {
  if (!grepl("^\\[.*\\].*$", x$raw)) {
    roxy_tag_warning(x, "Invalid memo format")
    return()
  }

  parsed <- stringi::stri_match(str = x$raw, regex = "\\[(.*)\\](.*)")[1, ]

  x$val <- list(
    header = parsed[[2]], 
    message = parsed[[3]]
  )
  x
}