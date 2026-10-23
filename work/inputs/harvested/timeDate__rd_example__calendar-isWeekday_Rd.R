# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: calendar-isWeekday.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 11

suppressPackageStartupMessages(library(timeDate))
## dates in april, current year
currentYear = getRmetricsOptions("currentYear")
tS = timeSequence(
   from = paste(currentYear, "-03-01", sep = ""),
   to = paste(currentYear, "-04-30", sep = ""))
tS

## subset of weekends
isWeekend(tS)
tS[isWeekend(tS)]