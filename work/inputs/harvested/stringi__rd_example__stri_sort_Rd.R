# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_sort.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 7

suppressPackageStartupMessages(library(stringi))
stri_sort(c('hladny', 'chladny'), locale='pl_PL')
stri_sort(c('hladny', 'chladny'), locale='sk_SK')
stri_sort(sample(LETTERS))
stri_sort(c(1, 100, 2, 101, 11, 10))  # lexicographic order
stri_sort(c(1, 100, 2, 101, 11, 10), numeric=TRUE)  # OK for integers
stri_sort(c(0.25, 0.5, 1, -1, -2, -3), numeric=TRUE)  # incorrect