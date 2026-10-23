# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: datasource.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 17

suppressPackageStartupMessages(library(readr))
# Literal csv
datasource("a,b,c\n1,2,3")
datasource(charToRaw("a,b,c\n1,2,3"))

# Strings
datasource(readr_example("mtcars.csv"))
datasource(readr_example("mtcars.csv.bz2"))
datasource(readr_example("mtcars.csv.zip"))

datasource("https://github.com/tidyverse/readr/raw/main/inst/extdata/mtcars.csv")


# Connection
con <- rawConnection(charToRaw("abc\n123"))
datasource(con)
close(con)