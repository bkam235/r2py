# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 15

suppressPackageStartupMessages(library(lifecycle))
add_two <- function(x, y, na.rm = TRUE) {
  if (!isTRUE(na.rm)) {
    lifecycle::deprecate_warn(
      when = "1.0.0", 
      what = "add_two(na.rm)",
      details = "Ability to retain missing values will be dropped in next release."
    )
  }
  
  sum(x, y, na.rm = na.rm)
}

add_two(1, NA, na.rm = TRUE)
add_two(1, NA, na.rm = FALSE)