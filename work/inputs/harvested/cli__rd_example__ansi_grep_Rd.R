# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_grep.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 6

suppressPackageStartupMessages(library(cli))
red_needle <- col_red("needle")
haystack <- c("foo", "needle", "foo")
green_haystack <- col_green(haystack)
ansi_grepl(red_needle, haystack)
ansi_grepl(red_needle, green_haystack)