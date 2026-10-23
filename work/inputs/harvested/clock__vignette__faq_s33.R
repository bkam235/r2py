# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: faq_s33
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\faq.R
# lines: 6

suppressPackageStartupMessages(library(clock))
ymdh <- year_month_day(2019, 1, 1:2, 1)

unclass(ymdh)

unclass(as_naive_time(ymdh))