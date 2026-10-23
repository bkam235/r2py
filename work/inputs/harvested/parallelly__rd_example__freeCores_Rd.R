# r2py crawler metadata
# package: parallelly
# source_type: rd_example
# topic: freeCores.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\parallelly\help
# lines: 7

suppressPackageStartupMessages(library(parallelly))
free <- freeCores()
print(free)


## Make availableCores() agile to the system load
options(parallelly.availableCores.custom = function() freeCores())