# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: weekday_code.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 8

suppressPackageStartupMessages(library(clock))
# Here we supply a western encoding to `weekday()`
x <- weekday(1:7)
x

# We can extract out the codes using different encodings
weekday_code(x, encoding = "western")
weekday_code(x, encoding = "iso")