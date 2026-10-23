# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: breaks_pretty.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 12

suppressPackageStartupMessages(library(scales))
one_month <- as.POSIXct(c("2020-05-01", "2020-06-01"))
demo_datetime(one_month)
demo_datetime(one_month, breaks = breaks_pretty(2))
demo_datetime(one_month, breaks = breaks_pretty(4))

# Tightly spaced date breaks often need custom labels too
demo_datetime(one_month, breaks = breaks_pretty(12))
demo_datetime(one_month,
  breaks = breaks_pretty(12),
  labels = label_date_short()
)