# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: holiday-NYSE.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 9

suppressPackageStartupMessages(library(timeDate))
holidayNYSE()  # current year
holidayNYSE(2008:2010)

## January 2, 2007 was a memorial day for president G.R. Ford,
##    not a regular public holiday
holidayNYSE(2007)
holidayNYSE(2007, type = "standard")
holidayNYSE(2007, type = "special")