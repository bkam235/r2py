# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s25
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 8

suppressPackageStartupMessages(library(stringr))
gettysburg <- "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal."

# base
cat(strwrap(gettysburg, width = 60), sep = "\n")

# stringr
cat(str_wrap(gettysburg, width = 60), "\n")