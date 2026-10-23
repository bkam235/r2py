# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: calendar-julian.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 26

suppressPackageStartupMessages(library(timeDate))
## julian
tC = timeCalendar(2022)
julian(tC)[1:3]
   
## atoms
atoms(tC)
   
## months
tC$month   # recommended 1 to 12
months(tC) # deprecated - will be changed to return month names, as base::months()

weekdays(tC)
weekdays(tC, TRUE)

## the dollar method
tC$year
tC$month
tC$day
tC$hour
tC$minute
tC$second
tC$weekday
tC$weekday0

tC$quarter