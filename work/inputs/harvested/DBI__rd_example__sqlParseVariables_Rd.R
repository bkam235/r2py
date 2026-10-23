# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: sqlParseVariables.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 12

suppressPackageStartupMessages(library(DBI))
# Use [] for quoting and no comments
sqlParseVariablesImpl("[?a]",
  list(sqlQuoteSpec("[", "]", "\\", FALSE)),
  list()
)

# Standard quotes, use # for commenting
sqlParseVariablesImpl("# ?a\n?b",
  list(sqlQuoteSpec("'", "'"), sqlQuoteSpec('"', '"')),
  list(sqlCommentSpec("#", "\n", FALSE))
)