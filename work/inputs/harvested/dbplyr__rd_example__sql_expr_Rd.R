# r2py crawler metadata
# package: dbplyr
# source_type: rd_example
# topic: sql_expr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dbplyr\help
# lines: 15

suppressPackageStartupMessages(library(dbplyr))
con <- simulate_dbi() # not necessary when writing translations

sql_expr(f(x + 1), con = con)
sql_expr(f("x", "y"), con = con)
sql_expr(f(x, y), con = con)

x <- ident("x")
sql_expr(f(!!x, y), con = con)

sql_expr(cast("x" %as% DECIMAL), con = con)
sql_expr(round(x) %::% numeric, con = con)

sql_call2("+", quote(x), 1, con = con)
sql_call2("+", "x", 1, con = con)