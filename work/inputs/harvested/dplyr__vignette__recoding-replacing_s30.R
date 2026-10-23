# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: recoding-replacing_s30
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\recoding-replacing.R
# lines: 9

suppressPackageStartupMessages(library(dplyr))
x <- c(1, 2, NA, 3, NA, 5)
y <- c(0, 3, 1, 4, 6, 7)

coalesce(x, 0)
replace_values(x, NA ~ 0)

coalesce(x, y)
replace_values(x, NA ~ y)