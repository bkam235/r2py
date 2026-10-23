# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: request-helper-functions_chunk5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\request-helper-functions.Rmd
# lines: 27

suppressPackageStartupMessages(library(gargle))
#| eval: false
# googledrive::
request_generate <- function(endpoint = character(),
                             params = list(),
                             key = NULL,
                             token = drive_token()) {
  ept <- .endpoints[[endpoint]]
  if (is.null(ept)) {
    stop_glue("\nEndpoint not recognized:\n  * {endpoint}")
  }

  ## modifications specific to googledrive package
  params$key <- key %||% params$key %||% drive_api_key()
  if (!is.null(ept$parameters$supportsTeamDrives)) {
    params$supportsTeamDrives <- TRUE
  }

  req <- gargle::request_develop(endpoint = ept, params = params)
  gargle::request_build(
    path = req$path,
    method = req$method,
    params = req$params,
    body = req$body,
    token = token
  )
}