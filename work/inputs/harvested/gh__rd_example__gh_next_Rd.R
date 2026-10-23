# r2py crawler metadata
# package: gh
# source_type: rd_example
# topic: gh_next.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gh\help
# lines: 7

suppressPackageStartupMessages(library(gh))
if (identical(Sys.getenv("IN_PKGDOWN"), "true")) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
x <- gh("/users")
vapply(x, "[[", character(1), "login")
x2 <- gh_next(x)
vapply(x2, "[[", character(1), "login")
}) # examplesIf