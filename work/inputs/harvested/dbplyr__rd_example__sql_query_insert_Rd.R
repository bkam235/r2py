# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: sql_query_insert.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 8

suppressPackageStartupMessages(library(dbplyr))
sql_query_upsert(
  con = simulate_postgres(),
  table = ident("airlines"),
  from = ident("df"),
  by = "carrier",
  update_cols = "name"
)