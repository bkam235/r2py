# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: httr_options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 8

suppressPackageStartupMessages(library(httr))
httr_options()
httr_options("post")

# Use curl_docs to read the curl documentation for each option.
# You can use either the httr or curl option name.
curl_docs("userpwd")
curl_docs("CURLOPT_USERPWD")