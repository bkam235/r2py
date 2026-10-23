# r2py crawler metadata
# package: tidyselect
# source_type: vignette
# topic: tidyselect_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\doc\tidyselect.R
# lines: 4

suppressPackageStartupMessages(library(tidyselect))
eval_select(rlang::expr(c(foo = mpg)), mtcars)

eval_rename(rlang::expr(c(foo = mpg)), mtcars)