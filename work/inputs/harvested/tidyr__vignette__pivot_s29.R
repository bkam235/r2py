# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s29
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 9

suppressPackageStartupMessages(library(tidyr))
weekdays <- c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

daily <- tibble(
  day = factor(c("Tue", "Thu", "Fri", "Mon"), levels = weekdays),
  value = c(2, 3, 1, 5)
)

daily