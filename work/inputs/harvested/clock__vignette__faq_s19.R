# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: faq_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\faq.R
# lines: 8

suppressPackageStartupMessages(library(clock))
y <- as.POSIXct(
  c("2019-01-01 01:00:00.1", "2019-01-01 01:00:00.3"), 
  "America/New_York"
)

# Oh dear!
y