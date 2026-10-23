# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: head_while.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 8

suppressPackageStartupMessages(library(purrr))
pos <- function(x) x >= 0
head_while(5:-5, pos)
tail_while(5:-5, negate(pos))

big <- function(x) x > 100
head_while(0:10, big)
tail_while(0:10, big)