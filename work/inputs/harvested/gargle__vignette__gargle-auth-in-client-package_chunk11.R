# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: gargle-auth-in-client-package_chunk11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\gargle-auth-in-client-package.Rmd
# lines: 12

suppressPackageStartupMessages(library(gargle))
#| eval: false
# googledrive::
drive_token <- function() {
  if (isFALSE(.auth$auth_active)) {
    return(NULL)
  }
  if (!drive_has_token()) {
    drive_auth()
  }
  httr::config(token = .auth$cred)
}