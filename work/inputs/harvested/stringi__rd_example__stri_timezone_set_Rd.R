# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_timezone_set.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 4

suppressPackageStartupMessages(library(stringi))
oldtz <- stri_timezone_set('Europe/Warsaw')
# ... many time zone-dependent operations
stri_timezone_set(oldtz) # restore previous default time zone