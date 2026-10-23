# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: transform_timespan.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 18

suppressPackageStartupMessages(library(scales))
# transform_timespan allows you to specify the time unit numeric data is
# interpreted in
trans_min <- transform_timespan("mins")
demo_timespan(seq(0, 100), trans = trans_min)
# Input already in difftime format is interpreted correctly
demo_timespan(as.difftime(seq(0, 100), units = "secs"), trans = trans_min)

if (require("hms")) {
  # transform_hms always assumes seconds
  hms <- round(runif(10) * 86400)
  t <- transform_hms()
  t$transform(hms)
  t$inverse(t$transform(hms))
  t$breaks(hms)
  # The break labels also follow the hms format
  demo_timespan(hms, trans = t)
}