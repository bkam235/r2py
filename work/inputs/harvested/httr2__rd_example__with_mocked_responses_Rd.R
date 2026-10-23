# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: with_mocked_responses.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 12

suppressPackageStartupMessages(library(httr2))
# This function should perform a response against google.com:
google <- function() {
  request("http://google.com") |>
    req_perform()
}

# But I can use a mock to instead return my own made up response:
my_mock <- function(req) {
  response(status_code = 403)
}
try(with_mocked_responses(my_mock, google()))