# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: faq_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\faq.R
# lines: 7

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01")
x

withr::with_timezone("America/New_York", {
  print(as.POSIXct(x))
})