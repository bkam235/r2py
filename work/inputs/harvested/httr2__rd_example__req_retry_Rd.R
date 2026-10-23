# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_retry.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 25

suppressPackageStartupMessages(library(httr2))
# google APIs assume that a 500 is also a transient error
request("http://google.com") |>
  req_retry(is_transient = \(resp) resp_status(resp) %in% c(429, 500, 503))

# use a constant 10s delay after every failure
request("http://example.com") |>
  req_retry(backoff = \(resp) 10)

# When rate-limited, GitHub's API returns a 403 with
# `X-RateLimit-Remaining: 0` and an Unix time stored in the
# `X-RateLimit-Reset` header. This takes a bit more work to handle:
github_is_transient <- function(resp) {
  resp_status(resp) == 403 &&
    identical(resp_header(resp, "X-RateLimit-Remaining"), "0")
}
github_after <- function(resp) {
  time <- as.numeric(resp_header(resp, "X-RateLimit-Reset"))
  time - unclass(Sys.time())
}
request("http://api.github.com") |>
  req_retry(
    is_transient = github_is_transient,
    after = github_after
  )