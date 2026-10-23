# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: namespace_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\namespace.R
# lines: 7

suppressPackageStartupMessages(library(roxygen2))
#' @export
bizarro.character <- function(x, ...) {
  letters <- strsplit(x, "")
  letters_rev <- lapply(letters, rev)
  vapply(letters_rev, paste, collapse = "", FUN.VALUE = character(1))
}