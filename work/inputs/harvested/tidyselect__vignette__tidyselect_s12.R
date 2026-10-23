# r2py crawler metadata
# package: tidyselect
# source_type: vignette
# topic: tidyselect_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\doc\tidyselect.R
# lines: 4

suppressPackageStartupMessages(library(tidyselect))
eval_select(rlang::expr(mpg), mtcars)

eval_select(rlang::expr(c(mpg:disp, vs)), mtcars)