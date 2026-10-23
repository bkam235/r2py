# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 9

suppressPackageStartupMessages(library(S7))
Empty <- new_class("Empty",
  properties = list(
    x = new_property(class_numeric, default = 0),
    y = new_property(class_character, default = ""),
    z = new_property(class_logical, default = NA)
  )
)
Empty()