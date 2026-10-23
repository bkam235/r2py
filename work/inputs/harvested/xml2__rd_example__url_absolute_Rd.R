# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: url_absolute.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 7

suppressPackageStartupMessages(library(xml2))
url_absolute(c(".", "..", "/", "/x"), "http://hadley.nz/a/b/c/d")

url_relative("http://hadley.nz/a/c", "http://hadley.nz")
url_relative("http://hadley.nz/a/c", "http://hadley.nz/")
url_relative("http://hadley.nz/a/c", "http://hadley.nz/a/b")
url_relative("http://hadley.nz/a/c", "http://hadley.nz/a/b/")