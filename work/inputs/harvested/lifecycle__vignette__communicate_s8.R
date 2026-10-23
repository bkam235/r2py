# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 11

suppressPackageStartupMessages(library(lifecycle))
add_two <- function(x, y) {
  lifecycle::deprecate_warn(
    "1.0.0", 
    "add_two()", 
    details = "This function is a special case of sum(); use it instead."
  )
  x + y
}

add_two(1, 2)