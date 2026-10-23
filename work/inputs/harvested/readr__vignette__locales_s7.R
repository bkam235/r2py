# r2py crawler metadata
# package: readr
# source_type: vignette
# topic: locales_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\doc\locales.R
# lines: 4

suppressPackageStartupMessages(library(readr))
parse_datetime("2001-10-10 20:10")
parse_datetime("2001-10-10 20:10", locale = locale(tz = "Pacific/Auckland"))
parse_datetime("2001-10-10 20:10", locale = locale(tz = "Europe/Dublin"))