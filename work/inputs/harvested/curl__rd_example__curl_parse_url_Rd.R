# r2py crawler metadata
# package: curl
# source_type: rd_example
# topic: curl_parse_url.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\help
# lines: 17

suppressPackageStartupMessages(library(curl))
url <- "https://jerry:secret@google.com:888/foo/bar?test=123#bla"
curl_parse_url(url)

# Resolve relative links from a baseurl
curl_parse_url("/somelink", baseurl = url)

# Paths get normalized
curl_parse_url("https://foobar.com/foo/bar/../baz/../yolo")$url

# Also normalizes URL-encoding (these URLs are equivalent):
url1 <- "https://ja.wikipedia.org/wiki/\u5bff\u53f8"
url2 <- "https://ja.wikipedia.org/wiki/%e5%af%bf%e5%8f%b8"
curl_parse_url(url1)$path
curl_parse_url(url2)$path
curl_parse_url(url1, decode = FALSE)$path
curl_parse_url(url1, decode = FALSE)$path