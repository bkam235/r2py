# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_datetime_format.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 7

suppressPackageStartupMessages(library(stringi))
x <- c('2015-02-28', '2015-02-29')
stri_datetime_parse(x, 'yyyy-MM-dd')
stri_datetime_parse(x, 'yyyy-MM-dd', lenient=TRUE)
stri_datetime_parse(x %s+% " 17:13", "yyyy-MM-dd HH:mm")
stri_datetime_parse('19 lipca 2015', 'date_long', locale='pl_PL')
stri_datetime_format(stri_datetime_now(), 'datetime_relative_medium')