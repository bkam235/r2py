# r2py crawler metadata
# package: stringi
# source_type: rd_example
# topic: stri_timezone_info.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringi\help
# lines: 6

suppressPackageStartupMessages(library(stringi))
stri_timezone_info()
stri_timezone_info(locale='sk_SK')
sapply(c('short', 'long', 'generic_short', 'generic_long',
         'gmt_short', 'gmt_long', 'common', 'generic_location'),
  function(e) stri_timezone_info('Europe/London', display_type=e))