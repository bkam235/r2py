# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: calendar-onOrAfter.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 11

suppressPackageStartupMessages(library(timeDate))
## date as character string
charvec = "2006-04-16"
   
## timeNdayOnOrAfter
# What date has the first Monday on or after March 15, 1986?
timeNdayOnOrAfter("1986-03-15", 1)
    
## timeNdayOnOrBefore
# What date has Friday on or before April 22, 1977?
timeNdayOnOrBefore("1986-03-15", 5)