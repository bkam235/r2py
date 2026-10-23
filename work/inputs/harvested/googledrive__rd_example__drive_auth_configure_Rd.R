# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_auth_configure.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 25

suppressPackageStartupMessages(library(googledrive))
# see and store the current user-configured OAuth client (probaby `NULL`)
(original_client <- drive_oauth_client())

# see and store the current user-configured API key (probaby `NULL`)
(original_api_key <- drive_api_key())

# the preferred way to configure your own client is via a JSON file
# downloaded from Google Developers Console
# this example JSON is indicative, but fake
path_to_json <- system.file(
  "extdata", "client_secret_installed.googleusercontent.com.json",
  package = "gargle"
)
drive_auth_configure(path = path_to_json)

# this is also obviously a fake API key
drive_auth_configure(api_key = "the_key_I_got_for_a_google_API")

# confirm the changes
drive_oauth_client()
drive_api_key()

# restore original auth config
drive_auth_configure(client = original_client, api_key = original_api_key)