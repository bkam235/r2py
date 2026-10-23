# r2py crawler metadata
# package: tidyselect
# source_type: vignette
# topic: tidyselect_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\doc\tidyselect.R
# lines: 7

suppressPackageStartupMessages(library(tidyselect))
fn <- function(arg) {
  expr <- rlang::enquo(arg)
  expr
}
user <- fn(1 + 2)
user