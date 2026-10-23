# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 20

suppressPackageStartupMessages(library(S7))
Range <- new_class("Range",
  properties = list(
    start = class_double,
    end = class_double
  ),
  validator = function(self) {
    if (length(self@start) != 1) {
      "@start must be length 1"
    } else if (length(self@end) != 1) {
      "@end must be length 1"
    } else if (self@end < self@start) {
      sprintf(
        "@end (%i) must be greater than or equal to @start (%i)",
        self@end,
        self@start
      )
    }
  }
)