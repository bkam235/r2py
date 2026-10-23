# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: req_perform_sequential.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 20

suppressPackageStartupMessages(library(httr2))
# One use of req_perform_sequential() is if the API allows you to request
# data for multiple objects, you want data for more objects than can fit
# in one request.
req <- request("https://api.restful-api.dev/objects")

# Imagine we have 50 ids:
ids <- sort(sample(100, 50))

# But the API only allows us to request 10 at time. So we first use split
# and some modulo arithmetic magic to generate chunks of length 10
chunks <- unname(split(ids, (seq_along(ids) - 1) %/% 10))

# Then we use lapply to generate one request for each chunk:
reqs <- chunks |> lapply(\(idx) req |> req_url_query(id = idx, .multi = "comma"))

# Then we can perform them all and get the results

resps <- reqs |> req_perform_sequential()
resps_data(resps, \(resp) resp_body_json(resp))