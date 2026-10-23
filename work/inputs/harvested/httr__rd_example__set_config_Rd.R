# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: set_config.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 6

suppressPackageStartupMessages(library(httr))
GET("http://google.com")
set_config(verbose())
GET("http://google.com")
reset_config()
GET("http://google.com")