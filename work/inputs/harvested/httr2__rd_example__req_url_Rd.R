# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_url.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 31

suppressPackageStartupMessages(library(httr2))
# Change complete url
req <- request("http://example.com")
req |> req_url("http://google.com")

# Use a relative url
req <- request("http://example.com/a/b/c")
req |> req_url_relative("..")
req |> req_url_relative("/d/e/f")

# Change url components
req |>
  req_url_path_append("a") |>
  req_url_path_append("b") |>
  req_url_path_append("search.html") |>
  req_url_query(q = "the cool ice")

# Modify individual query parameters
req <- request("http://example.com?a=1&b=2")
req |> req_url_query(a = 10)
req |> req_url_query(a = NULL)
req |> req_url_query(c = 3)

# Use .multi to control what happens with vector parameters:
req |> req_url_query(id = 100:105, .multi = "comma")
req |> req_url_query(id = 100:105, .multi = "explode")

# If you have query parameters in a list, use !!!
params <- list(a = "1", b = "2")
req |>
  req_url_query(!!!params, c = "3")