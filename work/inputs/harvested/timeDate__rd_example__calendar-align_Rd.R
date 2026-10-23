# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: calendar-align.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 15

suppressPackageStartupMessages(library(timeDate))
## align

# align bi-weekly with a 3 days offset
(tC <- timeCalendar())
align(tC, by = "2w", offset = "3d")

## alignDaily

# simple to use functions
alignDaily(tC)
alignDaily(tC, include.weekends = TRUE)

# align to end-of-month dates
alignMonthly(tC)