# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: calendar-firstDay.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 19

suppressPackageStartupMessages(library(timeDate))
## date as character string
charvec <- "2006-04-16"
myFinCenter <- getRmetricsOptions("myFinCenter")

## What date has the last day in a month for a given date?
timeLastDayInMonth(charvec, format = "%Y-%m-%d", 
  zone = myFinCenter, FinCenter = myFinCenter)
timeLastDayInMonth(charvec)
timeLastDayInMonth(charvec, FinCenter = "Zurich")
   
## What date has the first day in a month for a given date?
timeFirstDayInMonth(charvec)
    
## What date has the last day in a quarter for a given date?
timeLastDayInQuarter(charvec)
    
## What date has the first day in a quarter for a given date?
timeFirstDayInQuarter(charvec)