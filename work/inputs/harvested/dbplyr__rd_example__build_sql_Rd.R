# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: build_sql.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 11

suppressPackageStartupMessages(library(dbplyr))
con <- simulate_dbi()
build_sql("SELECT * FROM TABLE", con = con)
x <- "TABLE"
build_sql("SELECT * FROM ", x, con = con)
build_sql("SELECT * FROM ", ident(x), con = con)
build_sql("SELECT * FROM ", sql(x), con = con)

# http://xkcd.com/327/
name <- "Robert'); DROP TABLE Students;--"
build_sql("INSERT INTO Students (Name) VALUES (", name, ")", con = con)