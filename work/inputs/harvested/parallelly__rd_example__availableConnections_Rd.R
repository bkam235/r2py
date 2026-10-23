# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: availableConnections.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 5

suppressPackageStartupMessages(library(parallelly))
total <- availableConnections()
message("You can have ", total, " connections open in this R installation")
free <- freeConnections()
message("There are ", free, " connections remaining")