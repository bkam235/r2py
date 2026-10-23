# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 12

suppressPackageStartupMessages(library(stringr))
# base
sprintf("%30s", "hadley")
sprintf("%-30s", "hadley")
# "both" is not as straightforward

# stringr
rbind(
  str_pad("hadley", 30, "left"),
  str_pad("hadley", 30, "right"),
  str_pad("hadley", 30, "both")
)