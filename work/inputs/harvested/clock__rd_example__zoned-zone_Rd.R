# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: zoned-zone.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 16

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2019, 1, 1)
x <- as_zoned_time(as_naive_time(x), "America/New_York")
x

zoned_time_zone(x)

# Equivalent UTC time
zoned_time_set_zone(x, "UTC")

# To force a new time zone with the same printed time,
# convert to a naive time that has no implied time zone,
# then convert back to a zoned time in the new time zone.
nt <- as_naive_time(x)
nt
as_zoned_time(nt, "UTC")