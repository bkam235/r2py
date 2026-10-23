# r2py crawler metadata
# package: S7
# source_type: rd_example
# topic: validate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\help
# lines: 41

suppressPackageStartupMessages(library(S7))
# A range class might validate that the start is less than the end
Range <- new_class("Range",
  properties = list(start = class_double, end = class_double),
  validator = function(self) {
    if (self@start >= self@end) "start must be smaller than end"
  }
)
# You can't construct an invalid object:
try(Range(1, 1))

# And you can't create an invalid object with @<-
r <- Range(1, 2)
try(r@end <- 1)

# But what if you want to move a range to the right?
rightwards <- function(r, x) {
  r@start <- r@start + x
  r@end <- r@end + x
  r
}
# This function doesn't work because it creates a temporarily invalid state
try(rightwards(r, 10))

# This is the perfect use case for valid_eventually():
rightwards <- function(r, x) {
  valid_eventually(r, function(object) {
    object@start <- object@start + x
    object@end <- object@end + x
    object
  })
}
rightwards(r, 10)

# Alternatively, you can set multiple properties at once using props<-,
# which validates once at the end
rightwards <- function(r, x) {
  props(r) <- list(start = r@start + x, end = r@end + x)
  r
}
rightwards(r, 20)