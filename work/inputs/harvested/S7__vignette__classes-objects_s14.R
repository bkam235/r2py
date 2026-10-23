# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 13

suppressPackageStartupMessages(library(S7))
Range <- new_class("Range",
  properties = list(
    start = class_double,
    end = class_double,
    length = new_property(
      getter = function(self) self@end - self@start
    )
  )
)

x <- Range(start = 1, end = 10)
x