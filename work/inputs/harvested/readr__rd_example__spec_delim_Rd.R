# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: spec_delim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 14

suppressPackageStartupMessages(library(readr))
# Input sources -------------------------------------------------------------
# Retrieve specs from a path
spec_csv(system.file("extdata/mtcars.csv", package = "readr"))
spec_csv(system.file("extdata/mtcars.csv.zip", package = "readr"))

# Or directly from a string (must contain a newline)
spec_csv(I("x,y\n1,2\n3,4"))

# Column types --------------------------------------------------------------
# By default, readr guesses the columns types, looking at 1000 rows
# throughout the file.
# You can specify the number of rows used with guess_max.
spec_csv(system.file("extdata/mtcars.csv", package = "readr"), guess_max = 20)