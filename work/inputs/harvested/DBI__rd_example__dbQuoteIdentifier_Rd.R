# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbQuoteIdentifier.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 17

suppressPackageStartupMessages(library(DBI))
# Quoting ensures that arbitrary input is safe for use in a query
name <- "Robert'); DROP TABLE Students;--"
dbQuoteIdentifier(ANSI(), name)

# Use Id() to specify other components such as the schema
id_name <- Id(schema = "schema_name", table = "table_name")
id_name
dbQuoteIdentifier(ANSI(), id_name)

# SQL vectors are always passed through as is
var_name <- SQL("select")
var_name
dbQuoteIdentifier(ANSI(), var_name)

# This mechanism is used to prevent double escaping
dbQuoteIdentifier(ANSI(), dbQuoteIdentifier(ANSI(), name))