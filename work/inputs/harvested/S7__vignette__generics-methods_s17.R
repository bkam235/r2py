# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: generics-methods_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\generics-methods.R
# lines: 7

suppressPackageStartupMessages(library(S7))
mean <- new_generic("mean", "x", function(x, ..., na.rm = TRUE) {
  if (!identical(na.rm, TRUE) && !identical(na.rm = FALSE)) {
    stop("`na.rm` must be either TRUE or FALSE")
  }
  S7_dispatch()
})