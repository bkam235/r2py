# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: faq_s28
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\faq.R
# lines: 10

suppressPackageStartupMessages(library(clock))
raw <- c(
  "2015-12-31T23:59:59", 
  "2015-12-31T23:59:60", # A real leap second!
  "2016-01-01T00:00:00"
)

x <- sys_time_parse(raw)

x