# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_auth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 22

suppressPackageStartupMessages(library(googledrive))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
# load/refresh existing credentials, if available
# otherwise, go to browser for authentication and authorization
drive_auth()

# see user associated with current token
drive_user()

# force use of a token associated with a specific email
drive_auth(email = "jenny@example.com")
drive_user()

# force the OAuth web dance
drive_auth(email = NA)

# use a 'read only' scope, so it's impossible to edit or delete files
drive_auth(scopes = "drive.readonly")

# use a service account token
drive_auth(path = "foofy-83ee9e7c9c48.json")
}) # examplesIf