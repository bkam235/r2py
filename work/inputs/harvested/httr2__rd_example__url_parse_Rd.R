# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: url_parse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 9

suppressPackageStartupMessages(library(httr2))
url_parse("http://google.com/")
url_parse("http://google.com:80/")
url_parse("http://google.com:80/?a=1&b=2")
url_parse("http://username@google.com:80/path;test?a=1&b=2#40")

# You can parse a relative URL if you also provide a base url
url_parse("foo", "http://google.com/bar/")
url_parse("..", "http://google.com/bar/")