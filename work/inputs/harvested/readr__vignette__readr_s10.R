# r2py crawler metadata
# package: readr
# source_type: vignette
# topic: readr_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\doc\readr.R
# lines: 5

suppressPackageStartupMessages(library(readr))
mtcars_spec <- spec_csv(readr_example("mtcars.csv"))
mtcars_spec

cols_condense(mtcars_spec)