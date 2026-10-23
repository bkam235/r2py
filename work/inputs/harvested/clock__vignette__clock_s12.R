# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 6

suppressPackageStartupMessages(library(clock))
date_parse(
  "juillet 10, 2021", 
  format = "%B %d, %Y", 
  locale = clock_locale("fr")
)