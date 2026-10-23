# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: calendar_leap_year.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 22

suppressPackageStartupMessages(library(clock))
x <- year_month_day(c(2019:2024, NA))
calendar_leap_year(x)

# For year-quarter-day, the leap year typically aligns with the Gregorian
# leap year, unless the `start` is February, in which case the leap year is
# always 1 year after the Gregorian leap year
x <- year_quarter_day(2020:2021, start = clock_months$january)
calendar_leap_year(x)

x <- year_quarter_day(2020:2021, start = clock_months$february)
calendar_leap_year(x)

# With a January start, 2020 has the extra day
get_day(year_quarter_day(2020, 1:4, "last", start = clock_months$january))
get_day(year_quarter_day(2021, 1:4, "last", start = clock_months$january))
get_day(year_quarter_day(2022, 1:4, "last", start = clock_months$january))

# With a February start, 2021 has the extra day
get_day(year_quarter_day(2020, 1:4, "last", start = clock_months$february))
get_day(year_quarter_day(2021, 1:4, "last", start = clock_months$february))
get_day(year_quarter_day(2022, 1:4, "last", start = clock_months$february))