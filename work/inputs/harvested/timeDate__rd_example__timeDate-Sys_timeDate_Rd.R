# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: timeDate-Sys.timeDate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 12

suppressPackageStartupMessages(library(timeDate))
## direct
Sys.timeDate()

## Local Time in Zurich
Sys.timeDate(FinCenter = "Zurich")  

## transformed from "POSIX(c)t" with timeDate()
timeDate(Sys.time()) 
 
## Local Time in Zurich
timeDate(Sys.time(), FinCenter = "Zurich")