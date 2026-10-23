# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: generics-methods_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\generics-methods.R
# lines: 5

suppressPackageStartupMessages(library(S7))
date <- new_class("date", parent = class_double)
# Cheat by using the existing base .Date class
method(print, date) <- function(x) print(.Date(x))
date(c(1, 10, 100))