# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: timeDate-Calendar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 16

suppressPackageStartupMessages(library(timeDate))
## timeCalendar
   
# Current Year:
getRmetricsOptions("currentYear")

# 12 months of current year
timeCalendar() 

timeCalendar(m = c(9, 1, 8, 2), d = c(28, 15, 30, 9),
             y = c(1989, 2001, 2004, 1990), FinCenter = "GMT")

timeCalendar(m = c(9, 1, 8, 2), d = c(28, 15, 30, 9),
             y = c(1989, 2001, 2004, 1990), FinCenter = "Europe/Zurich")
             
timeCalendar(h = c(9, 14), min = c(15, 23))