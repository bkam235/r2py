# r2py crawler metadata
# package: readr
# source_type: vignette
# topic: locales_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\doc\locales.R
# lines: 6

suppressPackageStartupMessages(library(readr))
str(parse_guess("17:55:14"))
str(parse_guess("5:55:14 PM"))
# Example of a non-standard time
str(parse_guess("h5m55s14 PM"))
str(parse_guess("h5m55s14 PM", locale = locale(time_format = "h%Hm%Ms%S %p")))