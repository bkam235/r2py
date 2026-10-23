# r2py crawler metadata
# package: tidyselect
# source_type: vignette
# topic: tidyselect_s26
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\doc\tidyselect.R
# lines: 4

suppressPackageStartupMessages(library(tidyselect))
if_width <- function(n, vars = peek_vars(fn = "if_width")) {
  which(nchar(vars) == n)
}