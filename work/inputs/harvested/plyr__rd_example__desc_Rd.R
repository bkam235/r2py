# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: desc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 5

suppressPackageStartupMessages(library(plyr))
desc(1:10)
desc(factor(letters))
first_day <- seq(as.Date("1910/1/1"), as.Date("1920/1/1"), "years")
desc(first_day)