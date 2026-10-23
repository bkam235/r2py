# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: generics-methods_chunk11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\generics-methods.Rmd
# lines: 4

suppressPackageStartupMessages(library(S7))
length <- new_generic("length", "x", function(x) {
  S7_dispatch()
})