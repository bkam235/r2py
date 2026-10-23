# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: oauth-client-not-app_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\oauth-client-not-app.R
# lines: 16

suppressPackageStartupMessages(library(gargle))
(path_to_installed_client <- system.file(
  "extdata", "client_secret_installed.googleusercontent.com.json",
  package = "gargle"
))
jsonlite::prettify(scan(path_to_installed_client, what = character()))
(client <- gargle_oauth_client_from_json(path_to_installed_client))
class(client)

(path_to_web_client <- system.file(
  "extdata", "client_secret_web.googleusercontent.com.json",
  package = "gargle"
))
jsonlite::prettify(scan(path_to_web_client, what = character()))
(client <- gargle_oauth_client_from_json(path_to_web_client))
class(client)