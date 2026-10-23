# r2py crawler metadata
# package: S7
# source_type: vignette
# topic: classes-objects_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\S7\doc\classes-objects.R
# lines: 15

suppressPackageStartupMessages(library(S7))
Stopwatch <- new_class("Stopwatch", properties = list(
  start_time = new_property(
    class = class_POSIXct,
    default = quote(Sys.time())
  ),
  elapsed = new_property(
    getter = function(self) {
      difftime(Sys.time(), self@start_time, units = "secs")
    }
  )
))
args(Stopwatch)
round(Stopwatch()@elapsed)
round(Stopwatch(Sys.time() - 1)@elapsed)