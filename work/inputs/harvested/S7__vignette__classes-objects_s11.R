# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 8

suppressPackageStartupMessages(library(S7))
Empty <- new_class("Empty",
  properties = list(
    x = class_double,
    y = class_character,
    z = class_logical
  ))
Empty()