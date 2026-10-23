# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: oauth_app.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 6

suppressPackageStartupMessages(library(httr))
google_app <- oauth_app(
  "google",
  key = "123456789.apps.googleusercontent.com",
  secret = "abcdefghijklmnopqrstuvwxyz"
)