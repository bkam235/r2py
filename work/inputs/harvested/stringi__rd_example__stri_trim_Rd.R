# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_trim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 5

suppressPackageStartupMessages(library(stringi))
stri_trim_left('               aaa')
stri_trim_right('r-project.org/', '\\P{P}')
stri_trim_both(' Total of 23.5 bitcoins. ', '\\p{N}')
stri_trim_both(' Total of 23.5 bitcoins. ', '\\P{N}', negate=TRUE)