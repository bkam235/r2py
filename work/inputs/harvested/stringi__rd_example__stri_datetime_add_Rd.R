# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_datetime_add.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 13

suppressPackageStartupMessages(library(stringi))
x <- stri_datetime_now()
print(x)
stri_datetime_add(x, units='months') <- 2
print(x)

x <- stri_datetime_create(2025, 4, 20)
print(x)
stri_datetime_add(x, -2, units='months')
stri_datetime_add(x, 1, units='years')
stri_datetime_add(x, 1, units='years', locale='@calendar=hebrew')

stri_datetime_add(stri_datetime_create(2024, 1, 31), 1, units='months')