# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: lahman.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 16

suppressPackageStartupMessages(library(dbplyr))
# Connect to a local sqlite database, if already created

library(dplyr)

if (has_lahman("sqlite")) {
  lahman_sqlite()
  batting <- tbl(lahman_sqlite(), "Batting")
  batting
}

# Connect to a local postgres database with lahman database, if available
if (has_lahman("postgres")) {
  lahman_postgres()
  batting <- tbl(lahman_postgres(), "Batting")
}