# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_rand_shuffle.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 4

suppressPackageStartupMessages(library(stringi))
stri_rand_shuffle(c('abcdefghi', '0123456789'))
# you can do better than this with stri_rand_strings:
stri_rand_shuffle(rep(stri_paste(letters, collapse=''), 10))