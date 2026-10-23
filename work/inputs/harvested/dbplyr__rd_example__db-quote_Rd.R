# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: db-quote.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 6

suppressPackageStartupMessages(library(dbplyr))
con <- simulate_dbi()
sql_escape_logical(con, c(TRUE, FALSE, NA))
sql_escape_date(con, Sys.Date())
sql_escape_date(con, Sys.time())
sql_escape_raw(con, charToRaw("hi"))