# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: manage_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\manage.R
# lines: 5

suppressPackageStartupMessages(library(lifecycle))
data_frame <- function(...) {
  lifecycle::deprecate_warn("1.1.0", "data_frame()", "tibble()")
  tibble::tibble(...)
}