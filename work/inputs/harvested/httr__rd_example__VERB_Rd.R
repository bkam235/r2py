# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: VERB.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 11

suppressPackageStartupMessages(library(httr))
r <- VERB(
  "PROPFIND", "http://svn.r-project.org/R/tags/",
  add_headers(depth = 1), verbose()
)
stop_for_status(r)
content(r)


VERB("POST", url = "http://httpbin.org/post")
VERB("POST", url = "http://httpbin.org/post", body = "foobar")