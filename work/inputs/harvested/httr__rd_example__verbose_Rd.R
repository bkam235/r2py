# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: verbose.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 21

suppressPackageStartupMessages(library(httr))
GET("http://httpbin.org", verbose())
GET("http://httpbin.org", verbose(info = TRUE))

f <- function() {
  GET("http://httpbin.org")
}
with_verbose(f())
with_verbose(f(), info = TRUE)

# verbose() makes it easy to see exactly what POST requests send
POST_verbose <- function(body, ...) {
  POST("https://httpbin.org/post", body = body, verbose(), ...)
  invisible()
}
POST_verbose(list(x = "a", y = "b"))
POST_verbose(list(x = "a", y = "b"), encode = "form")
POST_verbose(FALSE)
POST_verbose(NULL)
POST_verbose("")
POST_verbose("xyz")