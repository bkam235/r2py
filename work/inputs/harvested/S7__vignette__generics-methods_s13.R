# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: generics-methods_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\generics-methods.R
# lines: 4

suppressPackageStartupMessages(library(S7))
foo <- new_generic("foo", "x", function(x, y, ...) {
  S7_dispatch()
})
