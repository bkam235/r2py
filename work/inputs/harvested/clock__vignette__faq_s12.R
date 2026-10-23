# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: faq_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\faq.R
# lines: 16

suppressPackageStartupMessages(library(clock))
try({
# There is a DST gap 1 second after 01:59:59,
# which jumps us straight to 03:00:00,
# skipping the 2 o'clock hour entirely

x %>%
  as_naive_time() %>%
  add_minutes(30) %>%
  as_zoned_time(zoned_time_zone(x))

x %>%
  as_sys_time() %>%
  add_minutes(30) %>%
  as_zoned_time(zoned_time_zone(x))
})