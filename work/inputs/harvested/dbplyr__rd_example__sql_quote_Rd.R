# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: sql_quote.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 4

suppressPackageStartupMessages(library(dbplyr))
sql_quote("abc", "'")
sql_quote("I've had a good day", "'")
sql_quote(c("abc", NA), "'")