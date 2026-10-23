# r2py crawler metadata
# package: roxygen2
# source_type: rd_example
# topic: namespace_roclet.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\help
# lines: 12

suppressPackageStartupMessages(library(roxygen2))
# The most common namespace tag is @export, which declares that a function
# is part of the external interface of your package
#' @export
foofy <- function(x, y, z) {
}

# You'll also often find global imports living in a file called
# R/{package}-package.R.
#' @importFrom magrittr %>%
#' @import rlang
NULL