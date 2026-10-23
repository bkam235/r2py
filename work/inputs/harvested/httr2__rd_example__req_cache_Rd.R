# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_cache.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 14

suppressPackageStartupMessages(library(httr2))
# GitHub uses HTTP caching for all raw files.
url <- paste0(
  "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/",
  "master/inst/extdata/penguins.csv"
)
# Here I set debug = TRUE so you can see what's happening
req <- request(url) |> req_cache(tempdir(), debug = TRUE)

# First request downloads the data
resp <- req |> req_perform()

# Second request retrieves it from the cache
resp <- req |> req_perform()