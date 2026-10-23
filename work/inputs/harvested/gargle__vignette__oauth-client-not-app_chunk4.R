# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: oauth-client-not-app_chunk4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\oauth-client-not-app.Rmd
# lines: 35

suppressPackageStartupMessages(library(gargle))
#| eval: false
# BEFORE
drive_auth_configure <- function(app, path, api_key) {
  # not showing this code
  .auth$set_app(app)
  # more code we're not showing
}

drive_oauth_app <- function() .auth$app

# AFTER
drive_auth_configure <- function(client, path, api_key, app = deprecated()) {
  if (lifecycle::is_present(app)) {
    lifecycle::deprecate_warn(
      "2.1.0",
      "drive_auth_configure(app)",
      "drive_auth_configure(client)"
    )
    drive_auth_configure(client = app, path = path, api_key = api_key)
  } 
  
  # not showing this code
  .auth$set_client(client)
  # more code we're not showing
}

drive_oauth_client <- function() .auth$client

drive_oauth_app <- function() {
  lifecycle::deprecate_warn(
    "2.1.0", "drive_oauth_app()", "drive_oauth_client()"
  )
  drive_oauth_client()
}