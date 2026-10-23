# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 20

suppressPackageStartupMessages(library(lifecycle))
#' Add two numbers
#' 
#' @description 
#' `r lifecycle::badge("deprecated")`
#' 
#' `add_two()` was renamed to `number_add()` to create a more
#' consistent API.
#' @keywords internal
#' @export
add_two <- function(foo, bar) {
  lifecycle::deprecate_warn("1.0.0", "add_two()", "number_add()")
  number_add(foo, bar)
}

# documentation goes here...
#' @export
number_add <- function(x, y) {
  x + y
}