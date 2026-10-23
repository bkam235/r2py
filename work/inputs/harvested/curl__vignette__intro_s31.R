# r2py crawler metadata
# package: curl
# source_type: vignette
# topic: intro_s31
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\curl\doc\intro.R
# lines: 9

suppressPackageStartupMessages(library(curl))
# Perform request
res <- new_handle() |>
  handle_setopt(copypostfields = "moo=moomooo") |>
  handle_setheaders("Content-Type"="text/moo", "Cache-Control"="no-cache", "User-Agent"="A cow") |>
  curl_fetch_memory(url = "https://hb.cran.dev/post")

# Parse response
res$content |> rawToChar() |> jsonlite::prettify()