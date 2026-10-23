# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: faq_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\faq.R
# lines: 17

suppressPackageStartupMessages(library(clock))
new_utc <- function(x) {
  class(x) <- c("POSIXct", "POSIXt")
  attr(x, "tzone") <- "UTC"
  x
}

year_2050 <- 2524608000
five_microseconds <- 0.000005

new_utc(year_2050)

# Oh no!
new_utc(year_2050 + five_microseconds)

# Represented internally as:
year_2050 + five_microseconds