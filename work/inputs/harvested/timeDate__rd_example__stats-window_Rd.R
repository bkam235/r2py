# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: stats-window.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 10

suppressPackageStartupMessages(library(timeDate))
## timeCalendar
# monthly dates in current year
tS = timeCalendar()
tS 
   
## window
# 2nd quarter window:
tS[4:6]
window(tS, tS[4], tS[6])