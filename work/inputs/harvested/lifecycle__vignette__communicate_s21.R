# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 11

suppressPackageStartupMessages(library(lifecycle))
add_two <- function(x, y, na_rm = TRUE, na.rm = deprecated()) {
  if (lifecycle::is_present(na.rm)) {
    lifecycle::deprecate_warn("1.0.0", "add_two(na.rm)", "add_two(na_rm)")
    na_rm <- na.rm
  }
  
  sum(x, y, na.rm = na_rm)
}

add_two(1, NA, na.rm = TRUE)