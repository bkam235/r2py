# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: S7_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\S7.R
# lines: 7

suppressPackageStartupMessages(library(S7))
Pet <- new_class("Pet",
  properties = list(
    name = class_character,
    age = class_numeric
  )
)