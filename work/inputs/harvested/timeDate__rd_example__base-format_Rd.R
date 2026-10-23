# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: base-format.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 8

suppressPackageStartupMessages(library(timeDate))
## timeCalendar
# Time Calendar 16:00
tC = timeCalendar() + 16*3600
tC
   
## format as ISO character string 
format(tC)