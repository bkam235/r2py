# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_isempty.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 4

suppressPackageStartupMessages(library(stringi))
stri_isempty(letters[1:3])
stri_isempty(c(',', '', 'abc', '123', '\u0105\u0104'))
stri_isempty(character(1))