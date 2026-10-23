# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_timezone_list.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 11

suppressPackageStartupMessages(library(stringi))
stri_timezone_list()
stri_timezone_list(offset=1)
stri_timezone_list(offset=5.5)
stri_timezone_list(offset=5.75)
stri_timezone_list(region='PL')
stri_timezone_list(region='US', offset=-10)

# Fetch information on all time zones
do.call(rbind.data.frame,
   lapply(stri_timezone_list(), function(tz) stri_timezone_info(tz)))