# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: timeDate-midnightStandard.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 5

suppressPackageStartupMessages(library(timeDate))
ch <- "2007-12-31 24:00"
midnightStandard(ch)
(ms2 <- midnightStandard2(ch))
class(ms2)