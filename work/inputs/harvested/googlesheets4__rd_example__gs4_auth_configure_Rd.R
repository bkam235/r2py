# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_auth_configure.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 25

suppressPackageStartupMessages(library(googlesheets4))
# see and store the current user-configured OAuth client (probably `NULL`)
(original_client <- gs4_oauth_client())

# see and store the current user-configured API key (probably `NULL`)
(original_api_key <- gs4_api_key())

# the preferred way to configure your own client is via a JSON file
# downloaded from Google Developers Console
# this example JSON is indicative, but fake
path_to_json <- system.file(
  "extdata", "client_secret_installed.googleusercontent.com.json",
  package = "gargle"
)
gs4_auth_configure(path = path_to_json)

# this is also obviously a fake API key
gs4_auth_configure(api_key = "the_key_I_got_for_a_google_API")

# confirm the changes
gs4_oauth_client()
gs4_api_key()

# restore original auth config
gs4_auth_configure(client = original_client, api_key = original_api_key)