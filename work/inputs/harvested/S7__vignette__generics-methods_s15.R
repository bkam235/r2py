# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: generics-methods_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\generics-methods.R
# lines: 10

suppressPackageStartupMessages(library(S7))
mean <- new_generic("mean", "x", function(x, ..., na.rm = TRUE) {
  S7_dispatch()
})
method(mean, class_integer) <- function(x, na.rm = TRUE) {
  if (na.rm) {
    x <- x[!is.na(x)]
  }
  sum(x) / length(x)
}