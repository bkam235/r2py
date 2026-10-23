# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_remove_empty.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 6

suppressPackageStartupMessages(library(stringi))
stri_remove_empty(stri_na2empty(c('a', NA, '', 'b')))
stri_remove_empty(c('a', NA, '', 'b'))
stri_remove_empty(c('a', NA, '', 'b'), TRUE)

stri_omit_empty_na(c('a', NA, '', 'b'))