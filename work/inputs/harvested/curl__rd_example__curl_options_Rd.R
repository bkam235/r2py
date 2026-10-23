# r2py crawler metadata
# package: curl
# source_type: rd_example
# topic: curl_options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\help
# lines: 11

suppressPackageStartupMessages(library(curl))
# Available options
curl_options()

# List proxy options
curl_options("proxy")

# Symbol table
curl_symbols("proxy")
# Curl/ssl version info
curl_version()