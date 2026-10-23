# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 14

suppressPackageStartupMessages(library(clock))
monday <- weekday(clock_weekdays$monday)

x <- as.Date(c("2019-01-01", "2019-02-01"))

date_shift(x, monday)

# With a date-time
y <- as.POSIXct(
  c("2019-01-01 02:30:30", "2019-02-01 05:20:22"), 
  "America/New_York"
)

date_shift(y, monday)