# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 28

suppressPackageStartupMessages(library(S7))
try({
prop_number <- new_property(
  class = class_double,
  validator = function(value) {
    if (length(value) != 1L) "must be length 1"
  }
)

Range <- new_class("Range",
  properties = list(
    start = prop_number,
    end = prop_number
  ),
  validator = function(self) {
    if (self@end < self@start) {
      sprintf(
        "@end (%i) must be greater than or equal to @start (%i)",
        self@end,
        self@start
      )
    }
  }
)

Range(start = c(1.5, 3.5))
Range(end = c(1.5, 3.5))
})