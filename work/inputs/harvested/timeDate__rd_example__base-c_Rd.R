# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: base-c.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 10

suppressPackageStartupMessages(library(timeDate))
## timeCalendar
# Create Character Vectors:
GMT = timeCalendar(zone = "GMT", FinCenter = "GMT") + 16*3600
ZUR = timeCalendar(zone = "GMT", FinCenter = "Zurich") + 16*3600
   
## c
# concatenate and replicate timeDate objects
sort(c(GMT, ZUR))
sort(c(ZUR, GMT))