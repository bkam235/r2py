# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: write_stream.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 8

suppressPackageStartupMessages(library(httr))
GET(
  "https://github.com/jeroen/data/raw/gh-pages/diamonds.json",
  write_stream(function(x) {
    print(length(x))
    length(x)
  })
)