# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 26

suppressPackageStartupMessages(library(S7))
Range <- new_class("Range",
  properties = list(
    start = class_double,
    end = class_double,
    length = new_property(
      class = class_double,
      getter = function(self) self@end - self@start,
      setter = function(self, value) {
        if (!length(value)) {
          # Do nothing if called with the constructor default
          # value for this property, a zero-length double vector.
          return(self)
        }
        self@end <- self@start + value
        self
      }
    )
  )
)

x <- Range(start = 1, end = 10)
x

x@length <- 5
x