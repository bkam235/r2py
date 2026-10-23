# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbUnquoteIdentifier.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 22

suppressPackageStartupMessages(library(DBI))
# Unquoting allows to understand the structure of a
# possibly complex quoted identifier
dbUnquoteIdentifier(
  ANSI(),
  SQL(c('"Catalog"."Schema"."Table"', '"Schema"."Table"', '"UnqualifiedTable"'))
)

# The returned object is always a list,
# also for Id objects
dbUnquoteIdentifier(ANSI(), Id("Catalog", "Schema", "Table"))

# Quoting and unquoting are inverses
dbQuoteIdentifier(
  ANSI(),
  dbUnquoteIdentifier(ANSI(), SQL("UnqualifiedTable"))[[1]]
)

dbQuoteIdentifier(
  ANSI(),
  dbUnquoteIdentifier(ANSI(), Id("Schema", "Table"))[[1]]
)