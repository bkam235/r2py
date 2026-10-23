# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: imap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 6

suppressPackageStartupMessages(library(purrr))
imap_chr(sample(10), paste)

imap_chr(sample(10), \(x, idx) paste0(idx, ": ", x))

iwalk(mtcars, \(x, idx) cat(idx, ": ", median(x), "\n", sep = ""))