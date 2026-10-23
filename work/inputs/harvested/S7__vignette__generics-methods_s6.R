# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: generics-methods_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\generics-methods.R
# lines: 4

suppressPackageStartupMessages(library(S7))
simple_print <- new_generic("simple_print", "x")
method(simple_print, class_double) <- function(x, digits = 3) {}
method(simple_print, class_character) <- function(x, max_length = 100) {}