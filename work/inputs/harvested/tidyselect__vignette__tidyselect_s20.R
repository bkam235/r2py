# r2py crawler metadata
# package: tidyselect
# source_type: vignette
# topic: tidyselect_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\doc\tidyselect.R
# lines: 4

suppressPackageStartupMessages(library(tidyselect))
x <- rlang::expr(print(peek_vars()))

invisible(eval_select(x, data = mtcars))