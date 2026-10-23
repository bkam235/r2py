# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 8

suppressPackageStartupMessages(library(stringr))
# base
trimws(" String with trailing and leading white space\t")
trimws("\n\nString with trailing and leading white space\n\n")

# stringr
str_trim(" String with trailing and leading white space\t")
str_trim("\n\nString with trailing and leading white space\n\n")