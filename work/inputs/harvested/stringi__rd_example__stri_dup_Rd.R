# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_dup.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 5

suppressPackageStartupMessages(library(stringi))
stri_dup('a', 1:5)
stri_dup(c('a', NA, 'ba'), 4)
stri_dup(c('abc', 'pqrst'), c(4, 2))
"a" %s*% 5