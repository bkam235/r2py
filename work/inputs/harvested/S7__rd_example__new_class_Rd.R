# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: new_class.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 40

suppressPackageStartupMessages(library(S7))
# Create an class that represents a range using a numeric start and end
Range <- new_class("Range",
  properties = list(
    start = class_numeric,
    end = class_numeric
  )
)
r <- Range(start = 10, end = 20)
r
# get and set properties with @
r@start
r@end <- 40
r@end

# S7 automatically ensures that properties are of the declared types:
try(Range(start = "hello", end = 20))

# But we might also want to use a validator to ensure that start and end
# are length 1, and that start is < end
Range <- new_class("Range",
  properties = list(
    start = class_numeric,
    end = class_numeric
  ),
  validator = function(self) {
    if (length(self@start) != 1) {
      "@start must be a single number"
    } else if (length(self@end) != 1) {
      "@end must be a single number"
    } else if (self@end < self@start) {
      "@end must be great than or equal to @start"
    }
  }
)
try(Range(start = c(10, 15), end = 20))
try(Range(start = 20, end = 10))

r <- Range(start = 10, end = 20)
try(r@start <- 25)