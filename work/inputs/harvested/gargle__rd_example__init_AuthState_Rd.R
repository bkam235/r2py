# r2py crawler metadata
# package: gargle
# source_type: rd_example
# topic: init_AuthState.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\help
# lines: 12

suppressPackageStartupMessages(library(gargle))
my_client <- gargle_oauth_client(
  id = "some_long_client_id",
  secret = "ssshhhhh_its_a_secret",
  name = "my-nifty-oauth-client"
)

init_AuthState(
  package = "my_package",
  client = my_client,
  api_key = "api_key_api_key_api_key",
)