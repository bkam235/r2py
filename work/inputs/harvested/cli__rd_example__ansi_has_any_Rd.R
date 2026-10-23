# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_has_any.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 4

suppressPackageStartupMessages(library(cli))
## The second one has style if ANSI colors are supported
ansi_has_any("foobar")
ansi_has_any(col_red("foobar"))