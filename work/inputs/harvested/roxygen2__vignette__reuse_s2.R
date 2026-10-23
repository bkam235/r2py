# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: reuse_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\reuse.R
# lines: 17

suppressPackageStartupMessages(library(roxygen2))
#' Trigonometric approximations
#' @param x Input, in radians.
#' @name trig
NULL

#' @rdname trig
#' @export
sin_ish <- function(x) x - x^3 / 6

#' @rdname trig
#' @export
cos_ish <- function(x) 1 - x^2 / 2

#' @rdname trig
#' @export
tan_ish <- function(x) x + x^3 / 3