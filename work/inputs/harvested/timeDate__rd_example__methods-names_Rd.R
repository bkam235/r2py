# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: methods-names.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 5

suppressPackageStartupMessages(library(timeDate))
td <- timeCalendar()
td
names(td) <- LETTERS[seq_along(td)]
td