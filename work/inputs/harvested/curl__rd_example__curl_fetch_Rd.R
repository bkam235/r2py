# r2py crawler metadata
# package: curl
# source_type: rd_example
# topic: curl_fetch.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\help
# lines: 30

suppressPackageStartupMessages(library(curl))
# Load in memory
res <- curl_fetch_memory("https://hb.cran.dev/cookies/set?foo=123&bar=ftw")
res$content

# Save to disk
res <- curl_fetch_disk("https://hb.cran.dev/stream/10", tempfile())
res$content
readLines(res$content)

# Stream with callback
drip_url <- "https://hb.cran.dev/drip?duration=3&numbytes=15&code=200"
res <- curl_fetch_stream(drip_url, function(x){
  cat(rawToChar(x))
})

# Async API
data <- list()
success <- function(res){
  cat("Request done! Status:", res$status, "\n")
  data <<- c(data, list(res))
}
failure <- function(msg){
  cat("Oh noes! Request failed!", msg, "\n")
}
curl_fetch_multi("https://hb.cran.dev/get", success, failure)
curl_fetch_multi("https://hb.cran.dev/status/418", success, failure)
curl_fetch_multi("https://urldoesnotexist.xyz", success, failure)
multi_run()
str(data)