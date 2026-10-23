# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: reuse_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\reuse.R
# lines: 4

suppressPackageStartupMessages(library(roxygen2))
alphabet <- function(n) {
  paste0("`", letters[1:n], "`", collapse = ", ")
}