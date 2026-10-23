# r2py crawler metadata
# package: vroom
# source_type: rd_example
# topic: guess_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\help
# lines: 12

suppressPackageStartupMessages(library(vroom))
# Logical vectors
 guess_type(c("FALSE", "TRUE", "F", "T"))
 # Integers and doubles
 guess_type(c("1","2","3"))
 guess_type(c("1.6","2.6","3.4"))
 # Numbers containing grouping mark
 guess_type("1,234,566")
 # ISO 8601 date times
 guess_type(c("2010-10-10"))
 guess_type(c("2010-10-10 01:02:03"))
 guess_type(c("01:02:03 AM"))