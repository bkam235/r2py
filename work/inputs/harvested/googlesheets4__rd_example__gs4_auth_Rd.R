# r2py crawler metadata
# package: googlesheets4
# source_type: rd_example
# topic: gs4_auth.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googlesheets4\help
# lines: 19

suppressPackageStartupMessages(library(googlesheets4))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
# load/refresh existing credentials, if available
# otherwise, go to browser for authentication and authorization
gs4_auth()

# indicate the specific identity you want to auth as
gs4_auth(email = "jenny@example.com")

# force a new browser dance, i.e. don't even try to use existing user
# credentials
gs4_auth(email = NA)

# use a 'read only' scope, so it's impossible to edit or delete Sheets
gs4_auth(scopes = "spreadsheets.readonly")

# use a service account token
gs4_auth(path = "foofy-83ee9e7c9c48.json")
}) # examplesIf