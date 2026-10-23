# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 13

suppressPackageStartupMessages(library(lifecycle))
#' @importFrom lifecycle deprecated
add_two <- function(x, y, na.rm = deprecated()) {
  if (lifecycle::is_present(na.rm)) {
    lifecycle::deprecate_warn(
      when = "1.0.0", 
      what = "add_two(na.rm)",
      details = "Ability to retain missing values will be dropped in next release."
    )
  }
  
  sum(x, y, na.rm = na.rm)
}