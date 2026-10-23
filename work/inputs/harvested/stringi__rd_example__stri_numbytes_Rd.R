# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_numbytes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 8

suppressPackageStartupMessages(library(stringi))
stri_numbytes(letters)
stri_numbytes(c('abc', '123', '\u0105\u0104'))


# this used to fail on Windows, where there were no native support
# for 4-bytes Unicode characters; see, however, stri_unescape_unicode():
stri_numbytes('\U001F600') # compare stri_length('\U001F600')