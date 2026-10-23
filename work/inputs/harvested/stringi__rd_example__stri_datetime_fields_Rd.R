# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_datetime_fields.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 6

suppressPackageStartupMessages(library(stringi))
stri_datetime_fields(stri_datetime_now())
stri_datetime_fields(stri_datetime_now(), locale='@calendar=hebrew')
stri_datetime_symbols(locale='@calendar=hebrew')$Month[
   stri_datetime_fields(stri_datetime_now(), locale='@calendar=hebrew')$Month
]