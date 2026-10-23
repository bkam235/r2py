# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: window-functions_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\window-functions.R
# lines: 9

suppressPackageStartupMessages(library(dplyr))
df <- data.frame(year = 2000:2005, value = (0:5) ^ 2)
scrambled <- df[sample(nrow(df)), ]

wrong <- mutate(scrambled, prev_value = lag(value))
arrange(wrong, year)

right <- mutate(scrambled, prev_value = lag(value, order_by = year))
arrange(right, year)