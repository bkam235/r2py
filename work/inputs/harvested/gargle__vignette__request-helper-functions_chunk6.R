# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: request-helper-functions_chunk6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\request-helper-functions.Rmd
# lines: 22

suppressPackageStartupMessages(library(gargle))
#| eval: false
# gargle::
request_make <- function(x, ..., user_agent = gargle_user_agent()) {
  stopifnot(is.character(x$method))
  method <- switch(
    x$method,
    GET    = httr::GET,
    POST   = httr::POST,
    PATCH  = httr::PATCH,
    PUT    = httr::PUT,
    DELETE = httr::DELETE,
    abort(glue("Not a recognized HTTP method: {bt(x$method)}"))
  )
  method(
    url = x$url,
    body = x$body,
    x$token,
    user_agent,
    ...
  )
}