# r2py crawler metadata
# package: roxygen2
# source_type: rd_example
# topic: rd_roclet.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\help
# lines: 13

suppressPackageStartupMessages(library(roxygen2))
#' The length of a string (in characters)
#'
#' @param x A character vector.
#' @returns An integer vector the same length as `x`.
#'   `NA` strings have `NA` length.
#' @seealso [nchar()]
#' @export
#' @examples
#' str_length(letters)
#' str_length(c("i", "like", "programming", NA))
str_length <- function(x) {
}