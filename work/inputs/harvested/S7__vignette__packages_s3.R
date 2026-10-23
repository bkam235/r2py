# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: packages_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\packages.R
# lines: 4

suppressPackageStartupMessages(library(S7))
.onLoad <- function(...) {
  S7::methods_register()
}