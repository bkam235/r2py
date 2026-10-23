# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 20

suppressPackageStartupMessages(library(scales))
date_range <- function(start, days) {
  start <- as.POSIXct(start)
  c(start, start + days * 24 * 60 * 60)
}

two_months <- date_range("2020-05-01", 60)
demo_datetime(two_months)
demo_datetime(two_months, labels = label_date("%m/%d"))
demo_datetime(two_months, labels = label_date("%e %b", locale = "fr"))
demo_datetime(two_months, labels = label_date("%e %B", locale = "es"))
# ggplot2 provides a short-hand:
demo_datetime(two_months, date_labels = "%m/%d")

# An alternative labelling system is label_date_short()
demo_datetime(two_months, date_breaks = "7 days", labels = label_date_short())
# This is particularly effective for dense labels
one_year <- date_range("2020-05-01", 365)
demo_datetime(one_year, date_breaks = "month")
demo_datetime(one_year, date_breaks = "month", labels = label_date_short())