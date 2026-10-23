# r2py crawler metadata
# package: gargle
# source_type: rd_example
# topic: request_develop.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\help
# lines: 55

suppressPackageStartupMessages(library(gargle))
## Example with a prepared endpoint
ept <- googledrive::drive_endpoints("drive.files.update")[[1]]
req <- request_develop(
  ept,
  params = list(
    fileId = "abc",
    addParents = "123",
    description = "Exciting File"
  )
)
req

req <- request_build(
  method = req$method,
  path = req$path,
  params = req$params,
  body = req$body,
  token = "PRETEND_I_AM_A_TOKEN"
)
req

## Example with no previous knowledge of the endpoint
## List a file's comments
## https://developers.google.com/drive/v3/reference/comments/list
req <- request_build(
  method = "GET",
  path = "drive/v3/files/{fileId}/comments",
  params = list(
    fileId = "your-file-id-goes-here",
    fields = "*"
  ),
  token = "PRETEND_I_AM_A_TOKEN"
)
req

# Example with no previous knowledge of the endpoint and no token
# use an API key for which the Places API is enabled!
API_KEY <- "1234567890"

# get restaurants close to a location in Vancouver, BC
req <- request_build(
  method = "GET",
  path = "maps/api/place/nearbysearch/json",
  params = list(
    location = "49.268682,-123.167117",
    radius = 100,
    type = "restaurant"
  ),
  key = API_KEY,
  base_url = "https://maps.googleapis.com"
)
resp <- request_make(req)
out <- response_process(resp)
vapply(out$results, function(x) x$name, character(1))