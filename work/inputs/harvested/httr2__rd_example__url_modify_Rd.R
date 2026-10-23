# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: url_modify.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 15

suppressPackageStartupMessages(library(httr2))
url_modify("http://hadley.nz", path = "about")
url_modify("http://hadley.nz", scheme = "https")
url_modify("http://hadley.nz/abc", path = "/cde")
url_modify("http://hadley.nz/abc", path = "")
url_modify("http://hadley.nz?a=1", query = "b=2")
url_modify("http://hadley.nz?a=1", query = list(c = 3))

url_modify_query("http://hadley.nz?a=1&b=2", c = 3)
url_modify_query("http://hadley.nz?a=1&b=2", b = NULL)
url_modify_query("http://hadley.nz?a=1&b=2", a = 100)

url_modify_relative("http://hadley.nz/a/b/c.html", "/d.html")
url_modify_relative("http://hadley.nz/a/b/c.html", "d.html")
url_modify_relative("http://hadley.nz/a/b/c.html", "../d.html")