# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: testing.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 7

suppressPackageStartupMessages(library(dbplyr))
test_register_src("sqlite", {
  DBI::dbConnect(RSQLite::SQLite(), ":memory:", create = TRUE)
})

test_frame(x = 1:3, y = 3:1)
test_load(mtcars)