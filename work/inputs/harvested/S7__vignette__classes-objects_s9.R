# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 7

suppressPackageStartupMessages(library(S7))
Range <- new_class("Range",
  properties = list(
    start = new_property(class_double),
    end = new_property(class_double)
  )
)