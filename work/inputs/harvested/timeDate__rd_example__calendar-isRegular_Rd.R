# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: calendar-isRegular.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 9

suppressPackageStartupMessages(library(timeDate))
tC <- timeCalendar(2023)
tC
isRegular(tC)
frequency(tC)

isMonthly(tC)
isQuarterly(tC)
isDaily(tC)