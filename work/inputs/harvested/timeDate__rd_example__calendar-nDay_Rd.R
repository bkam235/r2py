# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: calendar-nDay.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 6

suppressPackageStartupMessages(library(timeDate))
## What date is the second Monday in April 2004?
timeNthNdayInMonth("2004-04-01", 1, 2)

## What date has the last Tuesday in May, 1996?
timeLastNdayInMonth("1996-05-01", 2)