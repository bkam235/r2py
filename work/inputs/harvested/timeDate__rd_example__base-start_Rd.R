# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: base-start.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 20

suppressPackageStartupMessages(library(timeDate))
## timeCalendar
# Random Calendar Dates:
set.seed(1234)
tR = sample(timeCalendar())
sort(tR)
tR
    
## start | end
start(tR)
end(tR)
   
## the first and last time stamp
tR[1]
tR[length(tR)]
rev(tR)[1]
   
## the range
c(start(tR), end(tR))
range(tR)