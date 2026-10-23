# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: generics-methods_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\generics-methods.R
# lines: 6

suppressPackageStartupMessages(library(S7))
mean <- new_generic("mean", "x")
method(mean, class_numeric) <- function(x) {
  sum(x) / length(x)
}
mean(1:10)