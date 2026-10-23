# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_body_raw.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 11

suppressPackageStartupMessages(library(httr2))
resp <- request("https://httr2.r-lib.org") |> req_perform()
resp

resp |> resp_has_body()
resp |> resp_body_raw()
resp |> resp_body_string()

if (requireNamespace("xml2", quietly = TRUE)) {
  resp |> resp_body_html()
}