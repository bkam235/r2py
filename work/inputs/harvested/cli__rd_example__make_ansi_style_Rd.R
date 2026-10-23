# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: make_ansi_style.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 8

suppressPackageStartupMessages(library(cli))
make_ansi_style("orange")
make_ansi_style("#123456")
make_ansi_style("orange", bg = TRUE)

orange <- make_ansi_style("orange")
orange("foobar")
cat(orange("foobar"))