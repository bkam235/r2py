# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: GET.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 24

suppressPackageStartupMessages(library(httr))
GET("http://google.com/")

GET("http://google.com/", path = "search")
GET("http://google.com/", path = "search", query = list(q = "ham"))


# See what GET is doing with httpbin.org

url <- "http://httpbin.org/get"
GET(url)
GET(url, add_headers(a = 1, b = 2))
GET(url, set_cookies(a = 1, b = 2))
GET(url, add_headers(a = 1, b = 2), set_cookies(a = 1, b = 2))
GET(url, authenticate("username", "password"))
GET(url, verbose())


# You might want to manually specify the handle so you can have multiple
# independent logins to the same website.

google <- handle("http://google.com")
GET(handle = google, path = "/")
GET(handle = google, path = "search")