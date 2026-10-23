# r2py crawler metadata
# package: tidyselect
# source_type: vignette
# topic: syntax_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\doc\syntax.R
# lines: 8

suppressPackageStartupMessages(library(tidyselect))
select_loc <- function(data, ...) {
  eval_select(rlang::expr(c(...)), data)
}

rename_loc <- function(data, ...) {
  eval_rename(rlang::expr(c(...)), data)
}