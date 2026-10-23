# r2py crawler metadata
# package: desc
# source_type: rd_example
# topic: desc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\desc\help
# lines: 4

suppressPackageStartupMessages(library(desc))
desc(package = "desc")
DESCRIPTION <- system.file("DESCRIPTION", package = "desc")
desc(DESCRIPTION)