# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: with_config.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 8

suppressPackageStartupMessages(library(httr))
with_config(verbose(), {
  GET("http://had.co.nz")
  GET("http://google.com")
})

# Or even easier:
with_verbose(GET("http://google.com"))