# r2py crawler metadata
# package: rematch
# source_type: rd_example
# topic: re_match.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rematch\help
# lines: 9

suppressPackageStartupMessages(library(rematch))
dates <- c("2016-04-20", "1977-08-08", "not a date", "2016",
  "76-03-02", "2012-06-30", "2015-01-21 19:58")
isodate <- "([0-9]{4})-([0-1][0-9])-([0-3][0-9])"
re_match(text = dates, pattern = isodate)

# The same with named groups
isodaten <- "(?<year>[0-9]{4})-(?<month>[0-1][0-9])-(?<day>[0-3][0-9])"
re_match(text = dates, pattern = isodaten)