# r2py crawler metadata
# package: tidyselect
# source_type: vignette
# topic: tidyselect_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\doc\tidyselect.R
# lines: 5

suppressPackageStartupMessages(library(tidyselect))
with_data <- function(data, x) {
  expr <- rlang::enquo(x)
  rlang::eval_tidy(expr, data = data)
}