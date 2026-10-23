# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: S7_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\S7.R
# lines: 6

suppressPackageStartupMessages(library(S7))
Dog <- new_class("Dog", properties = list(
  name = class_character,
  age = class_numeric
))
Dog