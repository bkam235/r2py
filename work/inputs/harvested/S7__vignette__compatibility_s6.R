# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: compatibility_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\compatibility.R
# lines: 5

suppressPackageStartupMessages(library(S7))
new_rle <- new_class("rle", properties = list(
  lengths = class_integer,
  values = class_atomic
))