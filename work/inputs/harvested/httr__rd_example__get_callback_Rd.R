# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: get_callback.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 34

suppressPackageStartupMessages(library(httr))
## Log all HTTP requests to the screeen
req_logger <- function(req) {
  cat("HTTP request to", sQuote(req$url), "\n")
}

old <- set_callback("request", req_logger)
g1 <- GET("https://httpbin.org")
g2 <- GET("https://httpbin.org/ip")
set_callback("request", old)

## Log all HTTP requests and response status codes as well
req_logger2 <- function(req) {
  cat("HTTP request to", sQuote(req$url), "... ")
}
res_logger <- function(req, res) {
  cat(res$status_code, "\n")
}

old_req <- set_callback("request", req_logger2)
old_res <- set_callback("response", res_logger)
g3 <- GET("https://httpbin.org")
g4 <- GET("https://httpbin.org/ip")
set_callback("request", old_req)
set_callback("response", old_res)

## Return a recorded response, without performing the HTTP request
replay <- function(req) {
  if (req$url == "https://httpbin.org") g3
}
old_req <- set_callback("request", replay)
grec <- GET("https://httpbin.org")
grec$date == g3$date
set_callback("request", old_req)