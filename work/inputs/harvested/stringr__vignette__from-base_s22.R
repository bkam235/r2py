# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 9

suppressPackageStartupMessages(library(stringr))
x <- "This string is moderately long"

# stringr
rbind(
  str_trunc(x, 20, "right"),
  str_trunc(x, 20, "left"),
  str_trunc(x, 20, "center")
)