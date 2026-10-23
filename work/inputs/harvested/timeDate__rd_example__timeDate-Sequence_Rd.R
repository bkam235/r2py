# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: timeDate-Sequence.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 23

suppressPackageStartupMessages(library(timeDate))
## timeSequence

## autodetection of format
(t1 <- timeSequence(from = "2004-03-12", to = "2004-04-11"))

stopifnot( ## different formats even:
  identical(t1, timeSequence(from = "2004-03-12", to = "11-Apr-2004")),
  identical(t1, ## explicit format and FinCenter :
      timeSequence(from = "2004-03-12", to = "2004-04-11",
                   format = "%Y-%m-%d", FinCenter = "GMT")))

## observe "switch to summer time":
timeSequence(from = "2004-03-26 05:00:00", to = "2004-04-02 05:00:00",
             zone = "Europe/Zurich", FinCenter = "Europe/Zurich")

## ensure fixed clock time:
timeSequence(from = "2004-03-26 05:00:00", to = "2004-04-01 05:00:00",
             by = "DSTday", zone = "Europe/Zurich", FinCenter = "Europe/Zurich")

## on the day of DST change the time may not exist (notice 2004-03-28 00:00:00):
timeSequence(from = "2004-03-26 01:00:00", to = "2004-04-01 01:00:00",
             by = "DSTday", zone = "Europe/Zurich", FinCenter = "Europe/Zurich")