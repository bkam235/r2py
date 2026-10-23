# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: concat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 9

suppressPackageStartupMessages(library(crayon))
"foo" %+% "bar"

letters[1:10] %+% chr(1:10)

letters[1:10] %+% "-" %+% chr(1:10)

## This is empty (unlike for parse)
character() %+% "*"