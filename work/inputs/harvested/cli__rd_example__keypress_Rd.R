# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: keypress.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 5

suppressPackageStartupMessages(library(cli))
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
x <- keypress()
cat("You pressed key", x, "\n")
}) # examplesIf