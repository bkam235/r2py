# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 14

suppressPackageStartupMessages(library(S7))
Range <- new_class("Range",
  properties = list(
    start = class_numeric,
    end = class_numeric
  ),
  constructor = function(x) {
    new_object(S7_object(),
               start = min(x, na.rm = TRUE),
               end = max(x, na.rm = TRUE))
  }
)

Range(c(10, 5, 0, 2, 5, 7))