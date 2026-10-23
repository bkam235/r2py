# r2py crawler metadata
# package: generics
# source_type: rd_example
# topic: coercion-time-difference.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\generics\help
# lines: 7

suppressPackageStartupMessages(library(generics))
as.difftime(1:5, units = "secs")

as.difftime(c("01:55:22", "01:55:25"))

as.difftime("01", format = "%H")
as.difftime("01", format = "%H", units = "secs")