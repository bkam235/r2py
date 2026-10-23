# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.R
# lines: 8

suppressPackageStartupMessages(library(stringr))
jabberwocky <- str_c(
  "`Twas brillig, and the slithy toves ",
  "did gyre and gimble in the wabe: ",
  "All mimsy were the borogoves, ",
  "and the mome raths outgrabe. "
)
cat(str_wrap(jabberwocky, width = 40))