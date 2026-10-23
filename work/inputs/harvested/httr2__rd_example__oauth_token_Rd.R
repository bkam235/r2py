# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: oauth_token.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 4

suppressPackageStartupMessages(library(httr2))
oauth_token("abcdef")
oauth_token("abcdef", expires_in = 3600)
oauth_token("abcdef", refresh_token = "ghijkl")