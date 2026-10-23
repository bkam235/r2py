# r2py crawler metadata
# package: readr
# source_type: vignette
# topic: locales_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\doc\locales.R
# lines: 9

suppressPackageStartupMessages(library(readr))
parse_number("$1,234.56")
parse_number("$1.234,56", 
  locale = locale(decimal_mark = ",", grouping_mark = ".")
)

# readr is smart enough to guess that if you're using , for decimals then
# you're probably using . for grouping:
parse_number("$1.234,56", locale = locale(decimal_mark = ","))