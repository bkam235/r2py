# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: pluralization-helpers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 12

suppressPackageStartupMessages(library(cli))
nfile <- 0; cli_text("Found {no(nfile)} file{?s}.")

#> Found no files.

nfile <- 1; cli_text("Found {no(nfile)} file{?s}.")

#> Found 1 file.

nfile <- 2; cli_text("Found {no(nfile)} file{?s}.")

#> Found 2 files.