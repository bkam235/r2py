# r2py crawler metadata
# package: pkgdown
# source_type: rd_example
# topic: test-crayon.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pkgdown\help
# lines: 7

suppressPackageStartupMessages(library(pkgdown))
cat(cli::col_red("This is red"), "\n")
cat(cli::col_blue("This is blue"), "\n")

message(cli::col_green("This is green"))

warning(cli::style_bold("This is bold"))